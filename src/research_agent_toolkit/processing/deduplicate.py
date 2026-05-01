from __future__ import annotations

from research_agent_toolkit.schemas import CandidateItem
from research_agent_toolkit.verification.title_matcher import normalize_title

SOURCE_PRIORITY = {
    "PubMed": 100,
    "Crossref": 95,
    "Europe PMC": 90,
    "arXiv": 85,
    "Semantic Scholar": 80,
    "Hugging Face": 75,
    "Hugging Face Dataset": 75,
    "GitHub": 70,
    "Web Search": 40,
}


def canonical_key(item: CandidateItem) -> str:
    if item.doi:
        return f"doi:{item.doi.strip().lower()}"
    if item.arxiv_id:
        return f"arxiv:{item.arxiv_id.strip().lower()}"
    if item.pubmed_id:
        return f"pmid:{item.pubmed_id.strip().lower()}"
    if item.github_url:
        return f"github:{item.github_url.rstrip('/').lower()}"
    if item.huggingface_url:
        return f"hf:{item.huggingface_url.rstrip('/').lower()}"
    return f"title:{normalize_title(item.title)}"


def _merge(target: CandidateItem, other: CandidateItem) -> CandidateItem:
    if not target.abstract and other.abstract:
        target.abstract = other.abstract
    for attr in ["doi", "arxiv_id", "pubmed_id", "github_url", "huggingface_url", "project_url"]:
        if getattr(target, attr) is None and getattr(other, attr) is not None:
            setattr(target, attr, getattr(other, attr))
    if not target.authors and other.authors:
        target.authors = other.authors
    links = target.raw.setdefault("merged_links", [])
    if other.url and other.url != target.url:
        links.append({"source": other.source, "url": other.url})
    return target


def deduplicate_candidates(items: list[CandidateItem]) -> list[CandidateItem]:
    grouped: dict[str, CandidateItem] = {}
    title_map: dict[str, str] = {}
    for item in items:
        key = canonical_key(item)
        title_key = f"title:{normalize_title(item.title)}"
        if title_key in title_map:
            key = title_map[title_key]
        else:
            title_map[title_key] = key
        if key not in grouped:
            grouped[key] = item
            continue
        current = grouped[key]
        if SOURCE_PRIORITY.get(item.source, 0) > SOURCE_PRIORITY.get(current.source, 0):
            grouped[key] = _merge(item, current)
        else:
            grouped[key] = _merge(current, item)
    return list(grouped.values())

from __future__ import annotations

from datetime import date

from research_agent_toolkit.schemas import CandidateItem
from research_agent_toolkit.verification.date_checker import parse_date

NEURO_TERMS = ["mri", "pet", "tau", "amyloid", "fdg", "alzheimer", "ad", "neuroimaging", "pseudo-pet", "synthesis", "reconstruction"]
VLM_TERMS = ["medical", "biomedical", "radiology", "pathology", "vision-language", "vlm", "clip", "foundation model", "multimodal"]
REPRO_TERMS = ["github", "code", "weight", "weights", "model card", "dataset", "hugging face", "release"]
SOURCE_QUALITY = {
    "PubMed": 5,
    "Crossref": 5,
    "Europe PMC": 4.5,
    "arXiv": 4,
    "Semantic Scholar": 4,
    "Hugging Face": 4,
    "Hugging Face Dataset": 4,
    "GitHub": 3.5,
    "Web Search": 2.5,
}


def _score_terms(text: str, terms: list[str]) -> float:
    text = text.lower()
    hits = sum(1 for term in terms if term.lower() in text)
    return min(5.0, hits * 1.25)


def _timeliness(item: CandidateItem) -> float:
    value = item.published_date or item.updated_date
    parsed = parse_date(value)
    if parsed is None:
        return 2.5
    age = (date.today() - parsed).days
    if age <= 7:
        return 5.0
    if age <= 30:
        return 4.0
    if age <= 180:
        return 2.5
    return 1.0


def rank_candidate(item: CandidateItem) -> CandidateItem:
    text = " ".join([item.title, item.abstract, item.source, item.url or ""])
    if item.module == "neuro_pet":
        relevance = _score_terms(text, NEURO_TERMS)
        clinical = min(5.0, relevance + (1.0 if "alzheimer" in text.lower() or "tau" in text.lower() else 0.0))
    elif item.module == "medical_vlm":
        relevance = _score_terms(text, VLM_TERMS)
        clinical = min(5.0, relevance)
    else:
        relevance = max(_score_terms(text, NEURO_TERMS), _score_terms(text, VLM_TERMS)) * 0.8
        clinical = relevance
    novelty = 3.0 + min(2.0, _score_terms(text, ["new", "novel", "foundation", "diffusion", "transformer", "multimodal"]) / 2)
    reproducibility = _score_terms(text, REPRO_TERMS)
    if item.github_url or item.huggingface_url:
        reproducibility = max(reproducibility, 4.0)
    source_quality = SOURCE_QUALITY.get(item.source, 2.0)
    timeliness = _timeliness(item)
    priority = 20.0 * (0.40 * relevance + 0.20 * novelty + 0.15 * clinical + 0.10 * reproducibility + 0.10 * source_quality + 0.05 * timeliness)
    item.scores.relevance = round(relevance, 2)
    item.scores.novelty = round(novelty, 2)
    item.scores.clinical_or_research_value = round(clinical, 2)
    item.scores.reproducibility = round(reproducibility, 2)
    item.scores.source_quality = round(source_quality, 2)
    item.scores.timeliness = round(timeliness, 2)
    item.scores.priority = round(min(100.0, max(0.0, priority)), 2)
    item.why_include_zh = f"优先级 {item.scores.priority:.1f}/100；主题相关性 {item.scores.relevance:.1f}/5，来源质量 {item.scores.source_quality:.1f}/5。"
    return item


def rank_candidates(items: list[CandidateItem]) -> list[CandidateItem]:
    ranked = [rank_candidate(item) for item in items]
    return sorted(ranked, key=lambda x: x.scores.priority, reverse=True)

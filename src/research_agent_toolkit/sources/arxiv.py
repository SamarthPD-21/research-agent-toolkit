from __future__ import annotations

from typing import Any
from xml.etree import ElementTree as ET

import requests

from .utils import as_candidate, clean_html, module_from_topic, quote_query

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"


def search_arxiv(topic_name: str, keywords: list[str], days: int, config: dict[str, Any]) -> list:
    source_cfg = config.get("sources", {}).get("arxiv", {})
    max_results = int(source_cfg.get("max_results_per_query", 5))
    timeout = int(config.get("safety", {}).get("request_timeout_seconds", 20))
    module = module_from_topic(topic_name)
    results = []
    for keyword in keywords:
        query = quote_query(f'all:"{keyword}"')
        url = f"https://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
        try:
            response = requests.get(url, timeout=timeout, headers={"User-Agent": "research-agent-toolkit/1.0"})
            response.raise_for_status()
            root = ET.fromstring(response.text)
        except Exception:
            continue
        for entry in root.findall(f"{ATOM}entry"):
            title = clean_html(entry.findtext(f"{ATOM}title"))
            abstract = clean_html(entry.findtext(f"{ATOM}summary"))
            published = entry.findtext(f"{ATOM}published")
            updated = entry.findtext(f"{ATOM}updated")
            entry_id = entry.findtext(f"{ATOM}id") or ""
            arxiv_id = entry_id.rsplit("/", 1)[-1] if entry_id else None
            doi = entry.findtext(f"{ARXIV}doi")
            authors = [clean_html(a.findtext(f"{ATOM}name")) for a in entry.findall(f"{ATOM}author")]
            if not title or not entry_id:
                continue
            results.append(
                as_candidate(
                    prefix="arxiv",
                    module=module,
                    item_type="paper",
                    title=title,
                    authors=[a for a in authors if a],
                    source="arXiv",
                    published_date=published[:10] if published else None,
                    updated_date=updated[:10] if updated else None,
                    abstract=abstract,
                    url=entry_id,
                    doi=doi,
                    arxiv_id=arxiv_id,
                    raw={"keyword": keyword},
                )
            )
    return results

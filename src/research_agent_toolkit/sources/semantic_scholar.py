from __future__ import annotations

import os
from typing import Any

from .utils import as_candidate, module_from_topic, safe_get_json, since_date


def search_semantic_scholar(topic_name: str, keywords: list[str], days: int, config: dict[str, Any]) -> list:
    source_cfg = config.get("sources", {}).get("semantic_scholar", {})
    max_results = int(source_cfg.get("max_results_per_query", 5))
    timeout = int(config.get("safety", {}).get("request_timeout_seconds", 20))
    token_env = source_cfg.get("api_key_env")
    token = os.environ.get(str(token_env)) if token_env else None
    headers = {"User-Agent": "research-agent-toolkit/1.0"}
    if token:
        headers["x-api-key"] = token
    module = module_from_topic(topic_name)
    results = []
    since_year = since_date(days)[:4]
    for keyword in keywords:
        data = safe_get_json(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            headers=headers,
            params={
                "query": keyword,
                "limit": max_results,
                "year": f"{since_year}-",
                "fields": "title,authors,year,abstract,url,externalIds,publicationDate,venue,openAccessPdf",
            },
            timeout=timeout,
        )
        for record in ((data or {}).get("data") or [])[:max_results]:
            title = record.get("title") or ""
            if not title:
                continue
            external = record.get("externalIds") or {}
            doi = external.get("DOI")
            arxiv_id = external.get("ArXiv")
            pmid = external.get("PubMed")
            url = record.get("url") or (f"https://doi.org/{doi}" if doi else "")
            results.append(
                as_candidate(
                    prefix="semanticscholar",
                    module=module,
                    item_type="paper",
                    title=title,
                    authors=[a.get("name", "") for a in record.get("authors", []) if a.get("name")],
                    source="Semantic Scholar",
                    published_date=record.get("publicationDate") or str(record.get("year") or ""),
                    abstract=record.get("abstract") or "",
                    url=url,
                    doi=doi,
                    arxiv_id=arxiv_id,
                    pubmed_id=pmid,
                    raw=record,
                )
            )
    return results

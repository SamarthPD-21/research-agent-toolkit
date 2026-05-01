from __future__ import annotations

from typing import Any

from .utils import as_candidate, clean_html, module_from_topic, safe_get_json, since_date


def search_pubmed(topic_name: str, keywords: list[str], days: int, config: dict[str, Any]) -> list:
    source_cfg = config.get("sources", {}).get("pubmed", {})
    max_results = int(source_cfg.get("max_results_per_query", 5))
    timeout = int(config.get("safety", {}).get("request_timeout_seconds", 20))
    module = module_from_topic(topic_name)
    results = []
    since = since_date(days)
    for keyword in keywords:
        term = f'({keyword}) AND ("{since}"[Date - Publication] : "3000"[Date - Publication])'
        search = safe_get_json(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            params={"db": "pubmed", "term": term, "retmode": "json", "retmax": max_results, "sort": "pub date"},
            timeout=timeout,
        )
        ids = (((search or {}).get("esearchresult") or {}).get("idlist") or [])[:max_results]
        if not ids:
            continue
        summary = safe_get_json(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
            params={"db": "pubmed", "id": ",".join(ids), "retmode": "json"},
            timeout=timeout,
        )
        records = (summary or {}).get("result") or {}
        for pmid in ids:
            record = records.get(pmid) or {}
            title = record.get("title") or ""
            if not title:
                continue
            authors = [a.get("name", "") for a in record.get("authors", []) if a.get("name")]
            doi = None
            for article_id in record.get("articleids", []):
                if article_id.get("idtype") == "doi":
                    doi = article_id.get("value")
            results.append(
                as_candidate(
                    prefix="pubmed",
                    module=module,
                    item_type="paper",
                    title=clean_html(title),
                    authors=authors,
                    source="PubMed",
                    published_date=record.get("pubdate"),
                    url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    doi=doi,
                    pubmed_id=pmid,
                    raw=record,
                )
            )
    return results

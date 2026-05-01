from __future__ import annotations

from typing import Any

from .utils import as_candidate, module_from_topic, safe_get_json, since_date


def search_europe_pmc(topic_name: str, keywords: list[str], days: int, config: dict[str, Any]) -> list:
    source_cfg = config.get("sources", {}).get("europe_pmc", {})
    max_results = int(source_cfg.get("max_results_per_query", 5))
    timeout = int(config.get("safety", {}).get("request_timeout_seconds", 20))
    module = module_from_topic(topic_name)
    results = []
    since = since_date(days)
    for keyword in keywords:
        query = f'"{keyword}" FIRST_PDATE:[{since} TO 3000-01-01]'
        data = safe_get_json(
            "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
            params={"query": query, "format": "json", "pageSize": max_results, "sort": "FIRST_PDATE_D desc"},
            timeout=timeout,
        )
        records = (((data or {}).get("resultList") or {}).get("result") or [])[:max_results]
        for record in records:
            title = record.get("title") or ""
            if not title:
                continue
            doi = record.get("doi")
            pmid = record.get("pmid")
            url = f"https://europepmc.org/article/{record.get('source', 'MED')}/{record.get('id')}"
            results.append(
                as_candidate(
                    prefix="europepmc",
                    module=module,
                    item_type="paper",
                    title=title,
                    authors=[a.strip() for a in (record.get("authorString") or "").split(",") if a.strip()][:10],
                    source="Europe PMC",
                    published_date=record.get("firstPublicationDate") or record.get("pubYear"),
                    abstract=record.get("abstractText") or "",
                    url=url,
                    doi=doi,
                    pubmed_id=pmid,
                    raw=record,
                )
            )
    return results

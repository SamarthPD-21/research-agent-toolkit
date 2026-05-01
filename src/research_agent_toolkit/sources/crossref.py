from __future__ import annotations

from typing import Any

from .utils import as_candidate, module_from_topic, safe_get_json, since_date


def _date_parts(record: dict[str, Any], key: str) -> str | None:
    parts = (((record.get(key) or {}).get("date-parts") or [[]])[0])
    if not parts:
        return None
    year = int(parts[0])
    month = int(parts[1]) if len(parts) > 1 else 1
    day = int(parts[2]) if len(parts) > 2 else 1
    return f"{year:04d}-{month:02d}-{day:02d}"


def search_crossref(topic_name: str, keywords: list[str], days: int, config: dict[str, Any]) -> list:
    source_cfg = config.get("sources", {}).get("crossref", {})
    max_results = int(source_cfg.get("max_results_per_query", 5))
    timeout = int(config.get("safety", {}).get("request_timeout_seconds", 20))
    module = module_from_topic(topic_name)
    results = []
    since = since_date(days)
    for keyword in keywords:
        data = safe_get_json(
            "https://api.crossref.org/works",
            params={"query.title": keyword, "filter": f"from-pub-date:{since}", "sort": "published", "order": "desc", "rows": max_results},
            timeout=timeout,
        )
        items = (((data or {}).get("message") or {}).get("items") or [])[:max_results]
        for record in items:
            titles = record.get("title") or []
            title = titles[0] if titles else ""
            if not title:
                continue
            doi = record.get("DOI")
            authors = []
            for a in record.get("author", [])[:10]:
                name = " ".join(x for x in [a.get("given"), a.get("family")] if x)
                if name:
                    authors.append(name)
            url = record.get("URL") or (f"https://doi.org/{doi}" if doi else "")
            results.append(
                as_candidate(
                    prefix="crossref",
                    module=module,
                    item_type="paper",
                    title=title,
                    authors=authors,
                    source="Crossref",
                    published_date=_date_parts(record, "published-print") or _date_parts(record, "published-online") or _date_parts(record, "published"),
                    abstract=record.get("abstract") or "",
                    url=url,
                    doi=doi,
                    raw=record,
                )
            )
    return results

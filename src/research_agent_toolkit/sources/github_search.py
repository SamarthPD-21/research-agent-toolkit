from __future__ import annotations

from typing import Any

from .utils import as_candidate, module_from_topic, request_headers, safe_get_json


def search_github(topic_name: str, keywords: list[str], days: int, config: dict[str, Any]) -> list:
    source_cfg = config.get("sources", {}).get("github", {})
    max_results = int(source_cfg.get("max_results_per_query", 5))
    timeout = int(config.get("safety", {}).get("request_timeout_seconds", 20))
    headers = request_headers(source_cfg.get("token_env"))
    module = module_from_topic(topic_name)
    results = []
    for keyword in keywords:
        query = f'{keyword} pushed:>={__import__("datetime").date.today() - __import__("datetime").timedelta(days=days)}'
        data = safe_get_json(
            "https://api.github.com/search/repositories",
            headers=headers,
            params={"q": query, "sort": "updated", "order": "desc", "per_page": max_results},
            timeout=timeout,
        )
        for repo in ((data or {}).get("items") or [])[:max_results]:
            full_name = repo.get("full_name") or ""
            if not full_name:
                continue
            description = repo.get("description") or ""
            url = repo.get("html_url") or ""
            results.append(
                as_candidate(
                    prefix="github",
                    module=module,
                    item_type="code",
                    title=full_name,
                    source="GitHub",
                    updated_date=(repo.get("pushed_at") or repo.get("updated_at") or "")[:10],
                    abstract=description,
                    url=url,
                    github_url=url,
                    raw=repo,
                )
            )
    return results

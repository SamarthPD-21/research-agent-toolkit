from __future__ import annotations

import os
from typing import Any

import requests

from .utils import as_candidate, module_from_topic


def search_web(topic_name: str, keywords: list[str], days: int, config: dict[str, Any]) -> list:
    source_cfg = config.get("sources", {}).get("web_search", {})
    provider = source_cfg.get("provider", "tavily")
    if provider != "tavily":
        return []
    token_env = source_cfg.get("api_key_env")
    api_key = os.environ.get(str(token_env)) if token_env else None
    if not api_key:
        return []
    max_results = int(source_cfg.get("max_results_per_query", 5))
    timeout = int(config.get("safety", {}).get("request_timeout_seconds", 20))
    module = module_from_topic(topic_name)
    results = []
    for keyword in keywords:
        try:
            response = requests.post(
                "https://api.tavily.com/search",
                json={"api_key": api_key, "query": keyword, "max_results": max_results, "search_depth": "basic", "include_answer": False},
                timeout=timeout,
            )
            response.raise_for_status()
            data = response.json()
        except Exception:
            continue
        for record in (data.get("results") or [])[:max_results]:
            title = record.get("title") or ""
            url = record.get("url") or ""
            if not title or not url:
                continue
            results.append(
                as_candidate(
                    prefix="web",
                    module=module,
                    item_type="project_page",
                    title=title,
                    source="Web Search",
                    abstract=record.get("content") or "",
                    url=url,
                    raw=record,
                )
            )
    return results

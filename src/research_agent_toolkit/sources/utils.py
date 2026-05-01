from __future__ import annotations

import hashlib
import os
import re
from datetime import date, timedelta
from typing import Any
from urllib.parse import quote_plus

import requests

from research_agent_toolkit.schemas import CandidateItem


def make_id(prefix: str, value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8", errors="ignore")).hexdigest()[:16]
    return f"{prefix}:{digest}"


def join_keywords(keywords: list[str]) -> str:
    return " OR ".join(f'"{kw}"' if " " in kw else kw for kw in keywords)


def since_date(days: int) -> str:
    return (date.today() - timedelta(days=days)).isoformat()


def safe_get_json(url: str, *, headers: dict[str, str] | None = None, params: dict[str, Any] | None = None, timeout: int = 20) -> Any | None:
    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def request_headers(token_env: str | None = None) -> dict[str, str]:
    headers = {"User-Agent": "research-agent-toolkit/1.0"}
    if token_env:
        token = os.environ.get(token_env)
        if token:
            headers["Authorization"] = f"Bearer {token}"
    return headers


def module_from_topic(topic_name: str) -> str:
    if topic_name in {"neuro_pet", "medical_vlm"}:
        return topic_name
    return "indirect"


def clean_html(text: str | None) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def quote_query(query: str) -> str:
    return quote_plus(query)


def as_candidate(
    *,
    prefix: str,
    module: str,
    item_type: str,
    title: str,
    source: str,
    url: str,
    abstract: str = "",
    authors: list[str] | None = None,
    published_date: str | None = None,
    updated_date: str | None = None,
    doi: str | None = None,
    arxiv_id: str | None = None,
    pubmed_id: str | None = None,
    github_url: str | None = None,
    huggingface_url: str | None = None,
    raw: dict[str, Any] | None = None,
) -> CandidateItem:
    key = doi or arxiv_id or pubmed_id or url or title
    return CandidateItem(
        id=make_id(prefix, key),
        module=module,  # type: ignore[arg-type]
        item_type=item_type,  # type: ignore[arg-type]
        title=clean_html(title),
        authors=authors or [],
        source=source,
        published_date=published_date,
        updated_date=updated_date,
        abstract=clean_html(abstract),
        url=url,
        doi=doi,
        arxiv_id=arxiv_id,
        pubmed_id=pubmed_id,
        github_url=github_url,
        huggingface_url=huggingface_url,
        raw=raw or {},
    )

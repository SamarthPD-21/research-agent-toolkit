from __future__ import annotations

import re
from dataclasses import dataclass

import requests


@dataclass(slots=True)
class LinkCheckResult:
    accessible: bool
    status_code: int | None = None
    final_url: str | None = None
    error: str | None = None


def check_url(url: str, timeout: int = 20) -> LinkCheckResult:
    if not url:
        return LinkCheckResult(False, error="empty_url")
    headers = {"User-Agent": "research-agent-toolkit/1.0"}
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout, headers=headers)
        if response.status_code in {403, 405} or response.status_code >= 500:
            response = requests.get(url, allow_redirects=True, timeout=timeout, headers=headers, stream=True)
        return LinkCheckResult(200 <= response.status_code < 400, response.status_code, response.url)
    except Exception as exc:
        return LinkCheckResult(False, error=exc.__class__.__name__)


def fetch_page_title(url: str, timeout: int = 20) -> str | None:
    if not url:
        return None
    headers = {"User-Agent": "research-agent-toolkit/1.0"}
    try:
        response = requests.get(url, allow_redirects=True, timeout=timeout, headers=headers)
        response.raise_for_status()
    except Exception:
        return None
    match = re.search(r"<title[^>]*>(.*?)</title>", response.text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    title = re.sub(r"\s+", " ", match.group(1)).strip()
    return title or None

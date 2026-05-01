from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher


def normalize_title(title: str) -> str:
    text = unicodedata.normalize("NFKC", title or "").lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def titles_match(expected: str, observed: str, threshold: float = 0.78) -> bool:
    a = normalize_title(expected)
    b = normalize_title(observed)
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    ratio = SequenceMatcher(None, a, b).ratio()
    if ratio >= threshold:
        return True
    a_tokens = set(a.split())
    b_tokens = set(b.split())
    if not a_tokens or not b_tokens:
        return False
    overlap = len(a_tokens & b_tokens) / max(1, min(len(a_tokens), len(b_tokens)))
    return overlap >= 0.75 and len(a_tokens & b_tokens) >= 3

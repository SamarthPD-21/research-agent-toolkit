from __future__ import annotations

import logging
import re

SECRET_PATTERNS = [
    re.compile(r"(api[_-]?key|token|password|secret)=([^\s]+)", re.IGNORECASE),
]


def redact(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(lambda m: f"{m.group(1)}=***", redacted)
    return redacted


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s - %(message)s")

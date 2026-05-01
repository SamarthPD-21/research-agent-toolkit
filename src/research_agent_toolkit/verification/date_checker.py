from __future__ import annotations

import re
from datetime import date, datetime, timedelta


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    value = str(value).strip()
    if not value:
        return None
    patterns = ["%Y-%m-%d", "%Y-%m", "%Y", "%Y/%m/%d", "%d %b %Y", "%b %d, %Y"]
    for pattern in patterns:
        try:
            parsed = datetime.strptime(value[:10] if pattern == "%Y-%m-%d" else value, pattern)
            return parsed.date()
        except ValueError:
            pass
    match = re.search(r"(20\d{2}|19\d{2})[-/](\d{1,2})[-/](\d{1,2})", value)
    if match:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None


def date_is_recent_or_unknown(value: str | None, days: int) -> bool:
    parsed = parse_date(value)
    if parsed is None:
        return True
    return parsed >= date.today() - timedelta(days=days)

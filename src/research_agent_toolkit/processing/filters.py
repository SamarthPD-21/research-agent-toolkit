from __future__ import annotations

from collections import defaultdict
from typing import Any

from research_agent_toolkit.schemas import CandidateItem


def split_included_excluded(items: list[CandidateItem], config: dict[str, Any]) -> tuple[list[CandidateItem], list[CandidateItem]]:
    safety = config.get("safety", {})
    require_verified = bool(safety.get("require_verified_title", True))
    exclude_unverified = bool(safety.get("exclude_unverified_items", True))
    max_per_module = int(safety.get("max_items_per_module", 5))
    max_indirect = int(safety.get("max_indirect_items", 3))
    included: list[CandidateItem] = []
    excluded: list[CandidateItem] = []
    per_module: dict[str, int] = defaultdict(int)
    for item in items:
        if not item.title or not item.url:
            item.why_exclude_zh = "缺少标题或链接。"
            excluded.append(item)
            continue
        if require_verified and exclude_unverified and not (item.verification.title_matched and item.verification.url_accessible):
            item.why_exclude_zh = item.verification.notes or "链接或标题未通过核验。"
            excluded.append(item)
            continue
        limit = max_indirect if item.module == "indirect" else max_per_module
        if per_module[item.module] >= limit:
            item.why_exclude_zh = f"超过模块保留上限 {limit} 条。"
            excluded.append(item)
            continue
        included.append(item)
        per_module[item.module] += 1
    return included, excluded

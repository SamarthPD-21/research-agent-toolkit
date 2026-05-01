from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from research_agent_toolkit.processing.deduplicate import canonical_key
from research_agent_toolkit.schemas import CandidateItem


class HistoryStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.data = {"seen_items": []}

    def load(self) -> "HistoryStore":
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self.data = {"seen_items": []}
        return self

    def seen_keys(self) -> set[str]:
        return {item.get("canonical_id", "") for item in self.data.get("seen_items", []) if item.get("canonical_id")}

    def update(self, items: list[CandidateItem]) -> None:
        seen = {entry.get("canonical_id"): entry for entry in self.data.get("seen_items", []) if entry.get("canonical_id")}
        today = date.today().isoformat()
        for item in items:
            key = canonical_key(item)
            if key in seen:
                seen[key]["last_seen"] = today
            else:
                seen[key] = {"canonical_id": key, "title": item.title, "url": item.url, "first_seen": today, "last_seen": today, "source": item.source}
        self.data["seen_items"] = list(seen.values())

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

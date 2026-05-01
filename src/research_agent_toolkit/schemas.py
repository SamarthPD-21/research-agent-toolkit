from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

ModuleName = Literal["neuro_pet", "medical_vlm", "indirect"]
ItemType = Literal["paper", "model", "dataset", "code", "project_page", "release"]


@dataclass(slots=True)
class VerificationStatus:
    url_accessible: bool = False
    title_matched: bool = False
    date_verified: bool = False
    verification_source: str = "unknown"
    notes: str = ""


@dataclass(slots=True)
class Scores:
    relevance: float = 0.0
    novelty: float = 0.0
    clinical_or_research_value: float = 0.0
    reproducibility: float = 0.0
    source_quality: float = 0.0
    timeliness: float = 0.0
    priority: float = 0.0


@dataclass(slots=True)
class CandidateItem:
    id: str
    module: ModuleName
    item_type: ItemType
    title: str
    authors: list[str] = field(default_factory=list)
    source: str = "unknown"
    published_date: str | None = None
    updated_date: str | None = None
    abstract: str = ""
    url: str = ""
    doi: str | None = None
    arxiv_id: str | None = None
    pubmed_id: str | None = None
    github_url: str | None = None
    huggingface_url: str | None = None
    project_url: str | None = None
    verification: VerificationStatus = field(default_factory=VerificationStatus)
    scores: Scores = field(default_factory=Scores)
    summary_zh: str = ""
    why_include_zh: str = ""
    why_exclude_zh: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    def canonical_ids(self) -> list[str]:
        ids: list[str] = []
        if self.doi:
            ids.append(f"doi:{self.doi.strip().lower()}")
        if self.arxiv_id:
            ids.append(f"arxiv:{self.arxiv_id.strip().lower()}")
        if self.pubmed_id:
            ids.append(f"pmid:{self.pubmed_id.strip().lower()}")
        if self.github_url:
            ids.append(f"github:{self.github_url.rstrip('/').lower()}")
        if self.huggingface_url:
            ids.append(f"hf:{self.huggingface_url.rstrip('/').lower()}")
        if self.url:
            ids.append(f"url:{self.url.rstrip('/').lower()}")
        return ids

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CandidateItem":
        data = dict(data)
        verification = data.get("verification") or {}
        scores = data.get("scores") or {}
        if isinstance(verification, dict):
            data["verification"] = VerificationStatus(**verification)
        if isinstance(scores, dict):
            data["scores"] = Scores(**scores)
        return cls(**data)


@dataclass(slots=True)
class ReportResult:
    run_date: str
    search_window_days: int
    fallback_used: bool
    included: list[CandidateItem]
    excluded: list[CandidateItem]
    subject: str
    body_markdown: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_date": self.run_date,
            "search_window_days": self.search_window_days,
            "fallback_used": self.fallback_used,
            "included": [item.to_dict() for item in self.included],
            "excluded": [item.to_dict() for item in self.excluded],
            "email": {"subject": self.subject, "body_markdown": self.body_markdown},
        }

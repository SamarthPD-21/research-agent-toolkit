from __future__ import annotations

import json
from pathlib import Path

from research_agent_toolkit.schemas import CandidateItem, ReportResult


def write_run_outputs(report: ReportResult, candidates: list[CandidateItem], output_root: str | Path) -> Path:
    run_dir = Path(output_root) / report.run_date
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "email_zh.md").write_text(f"# {report.subject}\n\n{report.body_markdown}\n", encoding="utf-8")
    (run_dir / "report.json").write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    (run_dir / "candidates.json").write_text(json.dumps([item.to_dict() for item in candidates], ensure_ascii=False, indent=2), encoding="utf-8")
    (run_dir / "excluded.json").write_text(json.dumps([item.to_dict() for item in report.excluded], ensure_ascii=False, indent=2), encoding="utf-8")
    return run_dir

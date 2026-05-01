from pathlib import Path

from research_agent_toolkit.workflows.literature_monitor import run_literature_monitor


def test_workflow_dryrun_no_sources(tmp_path: Path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        f"""
topics:
  neuro_pet:
    enabled: true
    keywords: [MRI-to-PET]
sources:
  pubmed:
    enabled: false
llm:
  enabled: false
outputs:
  dir: {tmp_path / 'outputs'}
state:
  enabled: false
safety:
  dry_run: true
""",
        encoding="utf-8",
    )
    report = run_literature_monitor(cfg, dry_run=True)
    assert report.search_window_days in {7, 30}
    assert "一、本周期最重要结论" in report.body_markdown

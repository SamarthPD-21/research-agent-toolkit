from pathlib import Path

from research_agent_toolkit.config import load_config


def test_load_config_example(tmp_path: Path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """
topics:
  neuro_pet:
    enabled: true
    keywords: [MRI-to-PET]
sources: {}
""",
        encoding="utf-8",
    )
    config = load_config(cfg)
    assert config["schedule"]["default_days"] == 7
    assert config["topics"]["neuro_pet"]["enabled"] is True

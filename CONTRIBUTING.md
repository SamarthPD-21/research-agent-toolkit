# Contributing

Thank you for considering a contribution to Research Agent Toolkit.

## Development setup

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
```

## Contribution scope for v1.x

Good contributions include:

- new source clients;
- better title verification;
- better deduplication logic;
- new research-topic presets;
- documentation improvements;
- tests and mock responses;
- safer email delivery.

Please avoid adding features that scrape paid full text or bypass access restrictions.

## Pull request checklist

- [ ] Tests pass.
- [ ] No secrets are committed.
- [ ] New source clients handle network errors gracefully.
- [ ] New LLM logic does not invent factual fields.
- [ ] Documentation is updated.

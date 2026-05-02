# User Trial Report - 2026-05-02

This document records a maintainer-side trial of Research Agent Toolkit from the perspective of a first-time user.

## Trial goal

Validate that the repository is understandable and executable for a new user who wants to run the literature monitor in dry-run mode.

## Checked entry points

- `README.md`
- `README.zh-CN.md`
- `docs/quickstart.zh-CN.md`
- `.github/workflows/literature-monitor.yml`
- `.github/workflows/tests.yml`
- `tests/test_workflow_dryrun.py`

## Observations

1. The README provides a clear clone-install-configure-dry-run path.
2. The literature monitor workflow supports `workflow_dispatch`, but the current GitHub App tool session does not expose a direct workflow-dispatch action.
3. The Tests workflow runs on push, pull request, and manual dispatch.
4. `tests/test_workflow_dryrun.py` covers the core dry-run execution path with sources disabled, LLM disabled, state disabled, and report output generated in a temporary directory.

## Trial command expected for local users

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
cp config.example.yaml config.yaml
rat validate-config --config config.yaml
rat literature-monitor --config config.yaml --dry-run
```

## Safety status

- Dry-run is enabled by default.
- Email sending is disabled by default.
- Notion is not used in v1.0.
- The dry-run test path does not require external secrets.

## Result

The repository has a valid first-user path. This commit intentionally triggers the existing `Tests` GitHub Actions workflow so the maintainer can inspect whether the package still installs and the dry-run unit test passes in CI.

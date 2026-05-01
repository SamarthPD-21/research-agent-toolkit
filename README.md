# Research Agent Toolkit

[![Tests](https://github.com/linshuijin6/research-agent-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/linshuijin6/research-agent-toolkit/actions/workflows/tests.yml)
[![Literature Monitor](https://github.com/linshuijin6/research-agent-toolkit/actions/workflows/literature-monitor.yml/badge.svg)](https://github.com/linshuijin6/research-agent-toolkit/actions/workflows/literature-monitor.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Research Agent Toolkit** is an open-source automation toolkit for researchers who want AI-powered literature monitoring without relying on paid agent platforms.

The v1.0 release focuses on one production-ready workflow:

> Weekly literature and model-update monitoring for MRI-to-PET, Tau PET, Alzheimer's disease, medical vision-language models, medical CLIP-style models, GitHub releases, and Hugging Face model cards.

A Simplified Chinese README is available at [README.zh-CN.md](README.zh-CN.md).

## Why this project exists

Many researchers already use private AI agents to monitor literature, summarize papers, and send weekly reports. However, most students and labs do not have access to paid agent platforms. This repository turns a private-agent workflow into a reproducible, forkable, GitHub Actions based system.

The toolkit is designed for:

- biomedical engineering students;
- medical imaging researchers;
- PET (Positron Emission Tomography) / MRI (Magnetic Resonance Imaging) researchers;
- AI-for-science users who want scheduled literature digests;
- open-source maintainers who need a transparent, auditable research automation workflow.

## v1.0 features

- NeuroPET / MRI-to-PET / Tau PET / AD literature monitoring.
- Medical VLM (Vision-Language Model), medical CLIP (Contrastive Language-Image Pretraining), foundation-model, GitHub, and Hugging Face update monitoring.
- 7-day default search window, with automatic 30-day fallback when strong results are insufficient.
- Source verification and title matching before inclusion.
- DOI, arXiv ID, PubMed ID, normalized-title, GitHub URL, and Hugging Face URL deduplication.
- Relevance, novelty, reproducibility, source-quality, and timeliness ranking.
- Chinese weekly email report generation with a fixed six-section structure.
- OpenAI-compatible LLM provider support, including OpenAI, DeepSeek, Doubao, and other compatible endpoints.
- SMTP email delivery, with dry-run enabled by default.
- Optional Gmail API sender implementation.
- GitHub Actions scheduled workflow.
- JSON and Markdown artifacts for every run.
- No Notion integration in v1.0. Notion workflows are intentionally deferred to a later release.

## What it monitors

### Module A: NeuroPET / MRI-to-PET / Tau PET / AD

The default configuration monitors topics such as:

- MRI-to-PET synthesis;
- Tau PET prediction or analysis;
- amyloid PET and FDG PET;
- PET reconstruction or pseudo-PET generation;
- multimodal neuroimaging for Alzheimer's disease;
- deep learning methods involving PET and MRI.

### Module B: Medical VLM / medical CLIP / foundation-model updates

The default configuration monitors:

- medical vision-language models;
- biomedical CLIP-style models;
- radiology foundation models;
- GitHub repositories and releases;
- Hugging Face models and datasets;
- model cards, dataset cards, and project pages.

## Quick start

### 1. Fork or create the repository

Create a GitHub repository and upload this code, or clone it locally:

```bash
git clone https://github.com/linshuijin6/research-agent-toolkit.git
cd research-agent-toolkit
```

### 2. Install locally

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 3. Create your configuration

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` and set your topics, recipient, LLM provider, and email mode.

### 4. Validate configuration

```bash
rat validate-config --config config.yaml
```

### 5. Run in dry-run mode

```bash
rat literature-monitor --config config.yaml --dry-run
```

Generated files will be written to:

```text
outputs/YYYY-MM-DD/
```

Typical outputs:

```text
email_zh.md
report.json
candidates.json
excluded.json
```

### 6. Enable scheduled GitHub Actions

The default workflow runs every Monday at 00:00 UTC, which is 08:00 Beijing time.

```yaml
on:
  schedule:
    - cron: "0 0 * * 1"
  workflow_dispatch:
```

## Configuration

The main configuration file is `config.yaml`. A complete example is provided in `config.example.yaml`.

Minimal LLM settings:

```yaml
llm:
  provider: openai_compatible
  base_url_env: LLM_BASE_URL
  api_key_env: LLM_API_KEY
  model_env: LLM_MODEL
```

Example DeepSeek secrets:

```text
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=your_api_key
LLM_MODEL=deepseek-chat
```

Example OpenAI secrets:

```text
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your_api_key
LLM_MODEL=gpt-4o
```

## GitHub Secrets

Recommended secrets:

```text
LLM_BASE_URL
LLM_API_KEY
LLM_MODEL
SEMANTIC_SCHOLAR_API_KEY
HUGGINGFACE_TOKEN
SMTP_HOST
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
SMTP_FROM
```

`GITHUB_TOKEN` is automatically available in GitHub Actions. You do not need to create it manually.

## Email delivery

Email sending is disabled by default.

```yaml
email:
  enabled: false

safety:
  dry_run: true
```

To enable SMTP sending, set:

```yaml
email:
  enabled: true
  mode: smtp
```

and provide SMTP secrets in GitHub repository settings.

The default recipient in `config.example.yaml` is:

```text
1170414294@qq.com
```

## Report format

The Chinese weekly report always uses six sections:

1. 本周期最重要结论
2. MRI-to-PET / Tau PET / Alzheimer's disease 强相关论文
3. 医学图像大模型 / 医学视觉语言模型更新
4. 间接相关但可能有启发的论文或模型
5. 未纳入内容与原因
6. 下周建议关注关键词

## Ranking formula

Each candidate receives a 0-100 score:

\[
S = 20\left(0.40R + 0.20N + 0.15C + 0.10P + 0.10Q + 0.05T\right)
\]

LaTeX source:

```latex
S = 20\left(0.40R + 0.20N + 0.15C + 0.10P + 0.10Q + 0.05T\right)
```

Where:

- `R`: relevance;
- `N`: novelty;
- `C`: clinical or research value;
- `P`: reproducibility;
- `Q`: source quality;
- `T`: timeliness.

## Safety principles

- No API key is committed to the repository.
- No email password is committed to the repository.
- All secrets should be stored in GitHub Secrets or local environment variables.
- Dry-run is enabled by default.
- Source verification is required by default.
- The workflow never writes to Notion in v1.0.
- The workflow does not scrape paid full text or bypass website restrictions.
- The LLM is not allowed to invent paper titles, DOI values, code links, licenses, weights, or datasets.

## Roadmap

Planned future releases:

- v1.1: Gmail draft mode improvements.
- v1.2: MCP (Model Context Protocol) adapter.
- v1.3: Notion daily summary workflow.
- v1.4: Web dashboard.
- v1.5: More research-topic presets beyond biomedical imaging.

## Citation

If this project helps your research workflow, please cite the repository using the metadata in [CITATION.cff](CITATION.cff).

## License

Apache License 2.0. See [LICENSE](LICENSE).

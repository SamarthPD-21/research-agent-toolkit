# Research Agent Toolkit

[![Tests](https://github.com/linshuijin6/research-agent-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/linshuijin6/research-agent-toolkit/actions/workflows/tests.yml)
[![Literature Monitor](https://github.com/linshuijin6/research-agent-toolkit/actions/workflows/literature-monitor.yml/badge.svg)](https://github.com/linshuijin6/research-agent-toolkit/actions/workflows/literature-monitor.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Research Agent Toolkit** 是一个面向科研人员的开源 AI 自动化工具箱，用 GitHub Actions、网络检索、LLM 和邮件系统，把私有科研 Agent 工作流变成可复现、可 fork、可审计的开源项目。

> v1.0 专注于一个稳定工作流：**自动监控 MRI-to-PET、Tau PET、AD、医学图像大模型、医学 VLM、医学 CLIP、GitHub 项目和 Hugging Face 模型更新，并生成中文文献周报邮件。**

English README: [README.md](README.md)

---

## 你可以用它做什么

| 能力 | v1.0 状态 |
|---|---:|
| 定时文献监控 | 已支持 |
| NeuroPET / MRI-to-PET / Tau PET / AD 预设 | 已支持 |
| 医学 VLM / 医学 CLIP / foundation model 预设 | 已支持 |
| GitHub Actions 自动运行 | 已支持 |
| 中文周报邮件 | 已支持 |
| OpenAI-compatible LLM 后端 | 已支持 |
| SMTP 邮件发送 | 已支持，默认关闭 |
| Gmail API 发送 | 实验性支持 |
| Notion workflow | 计划中，v1.0 不包含 |

完整边界见：[v1.0 完整性审计](docs/completeness-audit.zh-CN.md)。

---

## 项目目标

很多科研人员已经在使用私有 AI Agent 定时监控文献、总结论文并发送邮件，但大部分学生和实验室没有 ChatGPT Team/Agent 这类付费平台。这个项目把私有 Agent 工作流转成一个可复制、可审计、可 fork、可长期维护的开源系统。

本项目适合：

- 生物医学工程研究生；
- 医学影像 AI 研究者；
- PET (Positron Emission Tomography，正电子发射断层成像) / MRI (Magnetic Resonance Imaging，磁共振成像) 方向研究者；
- 关注 MRI-to-PET、Tau PET、AD (Alzheimer's disease，阿尔茨海默病) 的用户；
- 想要低成本自动化文献监控的科研人员。

---

## 工作流概览

```mermaid
flowchart LR
    A[GitHub Actions 定时触发] --> B[检索文献和模型来源]
    B --> C[核验标题、日期和链接]
    C --> D[去重]
    D --> E[按相关性和可复现性排序]
    E --> F[生成中文周报邮件]
    F --> G[输出 Markdown / JSON]
    F --> H[可选 SMTP / Gmail 发送]
```

默认流程：

1. 先检索最近 7 天。
2. 强相关结果不足时扩展到最近 30 天。
3. 纳入正文前进行标题、日期和链接核验。
4. 每个模块最多保留 5 条强相关结果。
5. 每次运行输出 Markdown 和 JSON 文件。

---

## 监控内容

### 模块 A：NeuroPET / MRI-to-PET / Tau PET / AD

默认关注：

- MRI-to-PET 合成；
- pseudo-PET 生成；
- Tau PET 预测、分析和定量；
- amyloid PET、FDG PET 与 AD；
- PET 重建；
- 多模态神经影像；
- PET 与 MRI 结合的深度学习方法。

优先来源包括：

- Journal of Nuclear Medicine；
- IEEE Transactions on Radiation and Plasma Medical Sciences；
- European Journal of Nuclear Medicine and Molecular Imaging；
- IEEE Transactions on Medical Imaging；
- Medical Image Analysis；
- PubMed、Crossref、Europe PMC、arXiv 等。

### 模块 B：医学图像大模型 / 医学 VLM / 医学 CLIP

默认关注：

- medical vision-language model；
- biomedical VLM；
- medical CLIP；
- radiology foundation model；
- GitHub 仓库、release 和 README；
- Hugging Face 模型页、数据集页、model card 和 dataset card。

---

## 示例输出

每次运行生成的中文邮件固定包含六部分：

1. 本周期最重要结论
2. MRI-to-PET / Tau PET / Alzheimer's disease 强相关论文
3. 医学图像大模型 / 医学视觉语言模型更新
4. 间接相关但可能有启发的论文或模型
5. 未纳入内容与原因
6. 下周建议关注关键词

示例邮件见：[docs/demo-email.zh-CN.md](docs/demo-email.zh-CN.md)。

---

## 快速开始

```bash
git clone https://github.com/linshuijin6/research-agent-toolkit.git
cd research-agent-toolkit
python -m pip install --upgrade pip
pip install -e ".[dev]"
cp config.example.yaml config.yaml
rat validate-config --config config.yaml
rat literature-monitor --config config.yaml --dry-run
```

输出目录：

```text
outputs/YYYY-MM-DD/
```

常见输出：

```text
email_zh.md
report.json
candidates.json
excluded.json
```

更详细教程见：[docs/quickstart.zh-CN.md](docs/quickstart.zh-CN.md)。

---

## GitHub Actions 定时运行

v1.0 默认每周一 UTC 00:00 运行，对应北京时间每周一 08:00：

```yaml
on:
  schedule:
    - cron: "0 0 * * 1"
  workflow_dispatch:
```

你也可以在 GitHub Actions 页面手动触发。

---

## 配置 GitHub Secrets

建议在仓库 `Settings -> Secrets and variables -> Actions` 中添加：

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

`GITHUB_TOKEN` 由 GitHub Actions 自动提供，不需要手动添加。

---

## 模型配置示例

DeepSeek 示例：

```text
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=your_api_key
LLM_MODEL=deepseek-chat
```

OpenAI 示例：

```text
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=your_api_key
LLM_MODEL=gpt-4o
```

豆包或其他 OpenAI-compatible 服务也可以通过同样的 `base_url + api_key + model` 配置接入。

---

## 邮件发送

默认不会自动发送邮件：

```yaml
email:
  enabled: false

safety:
  dry_run: true
```

开启 SMTP 邮件发送：

```yaml
email:
  enabled: true
  mode: smtp
```

默认收件人是：

```text
1170414294@qq.com
```

---

## 评分公式

每条候选内容会得到 0-100 分：

\[
S = 20\left(0.40R + 0.20N + 0.15C + 0.10P + 0.10Q + 0.05T\right)
\]

LaTeX 代码：

```latex
S = 20\left(0.40R + 0.20N + 0.15C + 0.10P + 0.10Q + 0.05T\right)
```

其中：

- `R`：相关性；
- `N`：新颖性；
- `C`：临床或研究价值；
- `P`：可复现性；
- `Q`：来源质量；
- `T`：时效性。

---

## 安全原则

- 不提交任何 API Key。
- 不提交邮箱密码。
- 所有密钥应放入 GitHub Secrets 或本地环境变量。
- 默认 dry-run。
- 默认要求标题和链接核验。
- v1.0 不访问、不写入 Notion。
- 不爬取付费全文，不绕过网站权限限制。
- LLM 不允许编造论文标题、DOI、代码链接、权重、许可证或训练数据。

---

## Roadmap

后续计划：

- v1.1：增强 Gmail 草稿模式。
- v1.2：加入 MCP (Model Context Protocol，模型上下文协议) 适配层。
- v1.3：加入 Notion daily summary 工作流。
- v1.4：加入 Web dashboard。
- v1.5：加入更多科研方向 preset。

---

## 引用

如果本项目对你的研究工作流有帮助，请使用 [CITATION.cff](CITATION.cff) 中的信息引用本仓库。

## 许可证

Apache License 2.0，详见 [LICENSE](LICENSE)。

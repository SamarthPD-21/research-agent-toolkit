# 快速开始

1. 复制 `config.example.yaml` 为 `config.yaml`。
2. 设置 GitHub Secrets 或本地 `.env`。
3. 运行：

```bash
pip install -e ".[dev]"
rat validate-config --config config.yaml
rat literature-monitor --config config.yaml --dry-run
```

默认只生成报告，不发送邮件。

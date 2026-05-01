# LLM Provider 配置

本项目使用 OpenAI-compatible API 适配层。DeepSeek、OpenAI、豆包或其他兼容服务可以通过以下环境变量配置：

```text
LLM_BASE_URL
LLM_API_KEY
LLM_MODEL
```

如果未配置 LLM，本项目会使用确定性模板生成中文邮件，不会中断工作流。

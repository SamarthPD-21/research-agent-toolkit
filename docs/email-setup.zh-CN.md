# 邮件配置

v1.0 默认不会发送邮件。

SMTP 模式需要以下 Secrets：

```text
SMTP_HOST
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
SMTP_FROM
```

推荐先 dry-run，确认 `outputs/YYYY-MM-DD/email_zh.md` 内容无误后再开启发送。

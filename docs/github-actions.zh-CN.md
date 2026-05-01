# GitHub Actions 定时运行

`.github/workflows/literature-monitor.yml` 默认每周一 UTC 00:00 运行，对应北京时间 08:00。

你可以在 GitHub 的 Actions 页面手动触发 `workflow_dispatch`。

请先在仓库设置中添加必要 Secrets，再开启邮件发送。

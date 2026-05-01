# Security Policy

Research Agent Toolkit connects to external literature sources, LLM providers, GitHub, Hugging Face, and email services. Treat credentials carefully.

## Supported versions

Security fixes are applied to the latest release branch.

| Version | Supported |
| --- | --- |
| 1.x | Yes |

## Secrets

Never commit:

- LLM API keys;
- SMTP passwords;
- Gmail refresh tokens;
- Hugging Face tokens;
- Semantic Scholar API keys;
- private research logs;
- private Notion content.

Use GitHub Secrets for scheduled runs.

## Default safety behavior

The default configuration uses:

```yaml
email:
  enabled: false

safety:
  dry_run: true
  require_verified_title: true
  exclude_unverified_items: true
```

This means the workflow generates reports locally but does not send email unless explicitly enabled.

## v1.0 boundary

v1.0 does not access or write Notion. Notion-related features are planned for future releases.

## Reporting vulnerabilities

Open a private security advisory or contact the maintainer if you find a vulnerability.

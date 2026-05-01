from __future__ import annotations

import argparse
import sys

from research_agent_toolkit.config import ConfigError, load_config, validate_config
from research_agent_toolkit.delivery.smtp_email import send_smtp_email
from research_agent_toolkit.logging_utils import setup_logging
from research_agent_toolkit.workflows.literature_monitor import run_literature_monitor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rat", description="Research Agent Toolkit CLI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate-config", help="Validate config file.")
    validate.add_argument("--config", default="config.yaml")

    monitor = sub.add_parser("literature-monitor", help="Run literature monitor workflow.")
    monitor.add_argument("--config", default="config.yaml")
    monitor.add_argument("--days", type=int, default=None)
    monitor.add_argument("--dry-run", action="store_true", default=None)
    monitor.add_argument("--send", action="store_true", help="Override config and allow sending if email.enabled=true.")

    test_email = sub.add_parser("send-test-email", help="Send a test SMTP email using config.")
    test_email.add_argument("--config", default="config.yaml")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(args.verbose)
    try:
        if args.command == "validate-config":
            config = load_config(args.config)
            validate_config(config)
            print("Config OK")
            return 0
        if args.command == "literature-monitor":
            dry_run = args.dry_run
            if args.send:
                dry_run = False
            report = run_literature_monitor(args.config, days=args.days, dry_run=dry_run)
            print(report.subject)
            print(f"Included: {len(report.included)}; Excluded: {len(report.excluded)}; Window: {report.search_window_days} days")
            return 0
        if args.command == "send-test-email":
            config = load_config(args.config)
            send_smtp_email(config, "[Research Agent Toolkit] Test email", "This is a test email from Research Agent Toolkit.")
            print("Test email sent")
            return 0
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

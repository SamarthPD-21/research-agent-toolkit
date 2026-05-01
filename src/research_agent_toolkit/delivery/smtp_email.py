from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText
from typing import Any


class EmailConfigError(RuntimeError):
    pass


def send_smtp_email(config: dict[str, Any], subject: str, body: str) -> None:
    email_cfg = config.get("email", {})
    smtp_cfg = email_cfg.get("smtp", {})
    host = os.environ.get(str(smtp_cfg.get("host_env", "SMTP_HOST")), "")
    port = int(os.environ.get(str(smtp_cfg.get("port_env", "SMTP_PORT")), "465"))
    username = os.environ.get(str(smtp_cfg.get("username_env", "SMTP_USERNAME")), "")
    password = os.environ.get(str(smtp_cfg.get("password_env", "SMTP_PASSWORD")), "")
    sender = os.environ.get(str(smtp_cfg.get("from_env", "SMTP_FROM")), username)
    recipient = email_cfg.get("recipient")
    if not all([host, port, username, password, sender, recipient]):
        raise EmailConfigError("SMTP configuration is incomplete.")
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=30) as server:
            server.login(username, password)
            server.sendmail(sender, [recipient], msg.as_string())
    else:
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(sender, [recipient], msg.as_string())

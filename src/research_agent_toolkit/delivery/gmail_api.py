from __future__ import annotations

import base64
import os
from email.mime.text import MIMEText
from typing import Any

import requests


class GmailApiError(RuntimeError):
    pass


def _refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={"client_id": client_id, "client_secret": client_secret, "refresh_token": refresh_token, "grant_type": "refresh_token"},
        timeout=30,
    )
    response.raise_for_status()
    token = response.json().get("access_token")
    if not token:
        raise GmailApiError("Failed to refresh Gmail access token.")
    return token


def send_gmail_api_email(config: dict[str, Any], subject: str, body: str) -> None:
    email_cfg = config.get("email", {})
    gmail_cfg = email_cfg.get("gmail_api", {})
    client_id = os.environ.get(str(gmail_cfg.get("client_id_env", "GMAIL_CLIENT_ID")), "")
    client_secret = os.environ.get(str(gmail_cfg.get("client_secret_env", "GMAIL_CLIENT_SECRET")), "")
    refresh_token = os.environ.get(str(gmail_cfg.get("refresh_token_env", "GMAIL_REFRESH_TOKEN")), "")
    sender = os.environ.get(str(gmail_cfg.get("sender_env", "GMAIL_SENDER")), "")
    recipient = email_cfg.get("recipient")
    if not all([client_id, client_secret, refresh_token, sender, recipient]):
        raise GmailApiError("Gmail API configuration is incomplete.")
    access_token = _refresh_access_token(client_id, client_secret, refresh_token)
    msg = MIMEText(body, "plain", "utf-8")
    msg["To"] = recipient
    msg["From"] = sender
    msg["Subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    response = requests.post(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json={"raw": raw},
        timeout=30,
    )
    response.raise_for_status()

from __future__ import annotations

import os
from typing import Any

import requests


class LLMError(RuntimeError):
    pass


class OpenAICompatibleClient:
    def __init__(self, config: dict[str, Any]):
        llm_cfg = config.get("llm", {})
        self.base_url = os.environ.get(str(llm_cfg.get("base_url_env", "LLM_BASE_URL")), "").rstrip("/")
        self.api_key = os.environ.get(str(llm_cfg.get("api_key_env", "LLM_API_KEY")), "")
        self.model = os.environ.get(str(llm_cfg.get("model_env", "LLM_MODEL")), "")
        self.timeout = int(config.get("safety", {}).get("request_timeout_seconds", 20))

    @property
    def available(self) -> bool:
        return bool(self.base_url and self.api_key and self.model)

    def generate(self, messages: list[dict[str, str]], temperature: float = 0.2, max_tokens: int = 4096) -> str:
        if not self.available:
            raise LLMError("LLM configuration is incomplete.")
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise LLMError(str(exc)) from exc
        choices = data.get("choices") or []
        if not choices:
            raise LLMError("LLM response has no choices.")
        message = choices[0].get("message") or {}
        content = message.get("content")
        if not content:
            raise LLMError("LLM response has empty content.")
        return str(content)

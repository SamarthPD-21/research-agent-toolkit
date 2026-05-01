from __future__ import annotations

from typing import Any

from .utils import as_candidate, module_from_topic, request_headers, safe_get_json


def _hf_url(kind: str, model_id: str) -> str:
    if kind == "dataset":
        return f"https://huggingface.co/datasets/{model_id}"
    return f"https://huggingface.co/{model_id}"


def search_huggingface(topic_name: str, keywords: list[str], days: int, config: dict[str, Any]) -> list:
    source_cfg = config.get("sources", {}).get("huggingface", {})
    max_results = int(source_cfg.get("max_results_per_query", 5))
    timeout = int(config.get("safety", {}).get("request_timeout_seconds", 20))
    headers = request_headers(source_cfg.get("token_env"))
    module = module_from_topic(topic_name)
    results = []
    for keyword in keywords:
        models = safe_get_json(
            "https://huggingface.co/api/models",
            headers=headers,
            params={"search": keyword, "sort": "lastModified", "direction": -1, "limit": max_results},
            timeout=timeout,
        )
        for record in (models or [])[:max_results]:
            model_id = record.get("modelId") or record.get("id")
            if not model_id:
                continue
            url = _hf_url("model", model_id)
            results.append(
                as_candidate(
                    prefix="hf-model",
                    module=module,
                    item_type="model",
                    title=model_id,
                    source="Hugging Face",
                    updated_date=(record.get("lastModified") or "")[:10],
                    abstract=", ".join(record.get("tags") or []),
                    url=url,
                    huggingface_url=url,
                    raw=record,
                )
            )
        datasets = safe_get_json(
            "https://huggingface.co/api/datasets",
            headers=headers,
            params={"search": keyword, "sort": "lastModified", "direction": -1, "limit": max_results},
            timeout=timeout,
        )
        for record in (datasets or [])[: max(1, max_results // 2)]:
            dataset_id = record.get("id")
            if not dataset_id:
                continue
            url = _hf_url("dataset", dataset_id)
            results.append(
                as_candidate(
                    prefix="hf-dataset",
                    module=module,
                    item_type="dataset",
                    title=dataset_id,
                    source="Hugging Face Dataset",
                    updated_date=(record.get("lastModified") or "")[:10],
                    abstract=", ".join(record.get("tags") or []),
                    url=url,
                    huggingface_url=url,
                    raw=record,
                )
            )
    return results

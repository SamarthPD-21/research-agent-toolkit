from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path
from typing import Any, Callable

from research_agent_toolkit.config import load_config, source_enabled
from research_agent_toolkit.delivery.gmail_api import send_gmail_api_email
from research_agent_toolkit.delivery.markdown_writer import write_run_outputs
from research_agent_toolkit.delivery.smtp_email import send_smtp_email
from research_agent_toolkit.llm.openai_compatible import LLMError, OpenAICompatibleClient
from research_agent_toolkit.processing.deduplicate import deduplicate_candidates
from research_agent_toolkit.processing.filters import split_included_excluded
from research_agent_toolkit.processing.ranker import rank_candidates
from research_agent_toolkit.schemas import CandidateItem, ReportResult, VerificationStatus
from research_agent_toolkit.sources import (
    search_arxiv,
    search_crossref,
    search_europe_pmc,
    search_github,
    search_huggingface,
    search_pubmed,
    search_semantic_scholar,
    search_web,
)
from research_agent_toolkit.state.history import HistoryStore
from research_agent_toolkit.verification.date_checker import date_is_recent_or_unknown
from research_agent_toolkit.verification.link_checker import check_url, fetch_page_title
from research_agent_toolkit.verification.title_matcher import titles_match

LOGGER = logging.getLogger(__name__)

SourceFn = Callable[[str, list[str], int, dict[str, Any]], list[CandidateItem]]

SOURCE_REGISTRY: dict[str, SourceFn] = {
    "pubmed": search_pubmed,
    "arxiv": search_arxiv,
    "crossref": search_crossref,
    "europe_pmc": search_europe_pmc,
    "semantic_scholar": search_semantic_scholar,
    "github": search_github,
    "huggingface": search_huggingface,
    "web_search": search_web,
}


def _collect_candidates(config: dict[str, Any], days: int) -> list[CandidateItem]:
    items: list[CandidateItem] = []
    topics = config.get("topics", {})
    for topic_name, topic_cfg in topics.items():
        if not isinstance(topic_cfg, dict) or not topic_cfg.get("enabled", False):
            continue
        keywords = [str(x) for x in topic_cfg.get("keywords", [])]
        if not keywords:
            continue
        for source_name, source_fn in SOURCE_REGISTRY.items():
            if not source_enabled(config, source_name):
                continue
            try:
                found = source_fn(topic_name, keywords, days, config)
                LOGGER.info("source=%s topic=%s days=%s found=%s", source_name, topic_name, days, len(found))
                items.extend(found)
            except Exception as exc:
                LOGGER.warning("source=%s topic=%s failed: %s", source_name, topic_name, exc)
    return items


def _verify_item(item: CandidateItem, config: dict[str, Any], days: int) -> CandidateItem:
    safety = config.get("safety", {})
    timeout = int(safety.get("request_timeout_seconds", 20))
    allow_api_metadata = bool(safety.get("allow_api_metadata_as_verified", True))
    date_value = item.published_date or item.updated_date
    date_ok = date_is_recent_or_unknown(date_value, days)
    reliable_api_sources = {"PubMed", "Crossref", "Europe PMC", "arXiv", "Semantic Scholar", "GitHub", "Hugging Face", "Hugging Face Dataset"}
    if allow_api_metadata and item.source in reliable_api_sources:
        item.verification = VerificationStatus(
            url_accessible=bool(item.url),
            title_matched=bool(item.title),
            date_verified=date_ok,
            verification_source=item.source,
            notes="API metadata accepted as verified; direct page check may still be performed by users for strict auditing.",
        )
        return item
    link = check_url(item.url, timeout=timeout)
    observed_title = fetch_page_title(item.url, timeout=timeout) if link.accessible else None
    title_ok = titles_match(item.title, observed_title or "") if observed_title else False
    notes = ""
    if not link.accessible:
        notes = f"链接不可访问或请求失败：{link.error or link.status_code}。"
    elif not title_ok:
        notes = "页面标题与候选标题未能稳定匹配。"
    elif not date_ok:
        notes = "日期不在检索窗口内或日期核验失败。"
    item.verification = VerificationStatus(
        url_accessible=link.accessible,
        title_matched=title_ok,
        date_verified=date_ok,
        verification_source="direct_page",
        notes=notes,
    )
    return item


def _verify_candidates(items: list[CandidateItem], config: dict[str, Any], days: int) -> list[CandidateItem]:
    return [_verify_item(item, config, days) for item in items]


def _count_strong(items: list[CandidateItem]) -> int:
    return sum(1 for item in items if item.verification.url_accessible and item.verification.title_matched and item.scores.priority >= 45)


def _format_item(item: CandidateItem, index: int) -> str:
    authors = ", ".join(item.authors[:3]) + (" 等" if len(item.authors) > 3 else "") if item.authors else "作者未在元数据中提供"
    date_text = item.published_date or item.updated_date or "日期未明确"
    links = [f"主链接：{item.url}"]
    if item.doi:
        links.append(f"DOI：{item.doi}")
    if item.github_url:
        links.append(f"GitHub：{item.github_url}")
    if item.huggingface_url:
        links.append(f"Hugging Face：{item.huggingface_url}")
    summary = item.summary_zh or item.abstract[:280] or "暂无摘要；建议打开链接核对详情。"
    return (
        f"{index}. **{item.title}**\n"
        f"   - 来源：{item.source}；日期：{date_text}；作者：{authors}\n"
        f"   - 评分：{item.scores.priority:.1f}/100\n"
        f"   - 摘要：{summary}\n"
        f"   - 纳入理由：{item.why_include_zh}\n"
        f"   - " + "；".join(links) + "\n"
    )


def _fallback_email_body(included: list[CandidateItem], excluded: list[CandidateItem], days: int, fallback_used: bool) -> str:
    neuro = [x for x in included if x.module == "neuro_pet"]
    vlm = [x for x in included if x.module == "medical_vlm"]
    indirect = [x for x in included if x.module == "indirect"]
    window = f"最近 {days} 天" + ("（因强相关结果不足，已启用扩展检索）" if fallback_used else "")
    lines: list[str] = []
    lines.append("一、本周期最重要结论\n")
    if included:
        lines.append(f"本周期在{window}内共纳入 {len(included)} 条已验证候选内容。建议优先阅读评分最高且与当前 MRI-to-PET / Tau PET / AD 或医学图像大模型直接相关的条目。\n")
    else:
        lines.append(f"本周期在{window}内未发现足够强相关且通过核验的内容。已保留候选排除原因，建议下周继续关注同一关键词集合。\n")
    lines.append("二、MRI-to-PET / Tau PET / Alzheimer's disease 强相关论文\n")
    lines.append("\n".join(_format_item(item, i + 1) for i, item in enumerate(neuro)) if neuro else "本周期未纳入该模块强相关论文。\n")
    lines.append("三、医学图像大模型 / 医学视觉语言模型更新\n")
    lines.append("\n".join(_format_item(item, i + 1) for i, item in enumerate(vlm)) if vlm else "本周期未纳入该模块强相关更新。\n")
    lines.append("四、间接相关但可能有启发的论文或模型\n")
    lines.append("\n".join(_format_item(item, i + 1) for i, item in enumerate(indirect)) if indirect else "本周期未纳入间接相关内容。\n")
    lines.append("五、未纳入内容与原因\n")
    if excluded:
        lines.append("\n".join(f"- {item.title or '未命名条目'}：{item.why_exclude_zh or item.verification.notes or '未通过筛选。'}" for item in excluded[:20]) + "\n")
    else:
        lines.append("无。\n")
    lines.append("六、下周建议关注关键词\n")
    lines.append("- MRI-to-PET synthesis / pseudo-PET / Tau PET / amyloid PET / FDG PET reconstruction\n- Alzheimer's disease multimodal neuroimaging / PET-MRI deep learning\n- medical vision-language model / medical CLIP / radiology foundation model\n- Hugging Face medical imaging model card / GitHub medical VLM release\n")
    return "\n".join(lines)


def _build_email_with_llm(config: dict[str, Any], included: list[CandidateItem], excluded: list[CandidateItem], days: int, fallback_used: bool) -> str:
    if not config.get("llm", {}).get("enabled", True):
        return _fallback_email_body(included, excluded, days, fallback_used)
    client = OpenAICompatibleClient(config)
    if not client.available:
        return _fallback_email_body(included, excluded, days, fallback_used)
    payload = {
        "search_window_days": days,
        "fallback_used": fallback_used,
        "included": [item.to_dict() for item in included],
        "excluded": [item.to_dict() for item in excluded[:20]],
    }
    system_prompt = (
        "你是面向生物医学工程研究生的神经影像与医学 AI 文献监控助手。"
        "只能基于输入 JSON 中已验证的条目生成中文周报，不得编造论文、链接、DOI、权重、许可证或实验结论。"
        "邮件必须包含六部分：一、本周期最重要结论；二、MRI-to-PET / Tau PET / Alzheimer's disease 强相关论文；"
        "三、医学图像大模型 / 医学视觉语言模型更新；四、间接相关但可能有启发的论文或模型；"
        "五、未纳入内容与原因；六、下周建议关注关键词。"
    )
    try:
        return client.generate(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            temperature=float(config.get("llm", {}).get("temperature", 0.2)),
            max_tokens=int(config.get("llm", {}).get("max_tokens", 6000)),
        )
    except LLMError as exc:
        LOGGER.warning("LLM generation failed; using deterministic fallback: %s", exc)
        return _fallback_email_body(included, excluded, days, fallback_used)


def _subject(config: dict[str, Any], run_date: str) -> str:
    prefix = config.get("email", {}).get("subject_prefix", "[NeuroPET-MRI Weekly]")
    return f"{prefix} MRI-to-PET / Tau PET / CLIP 文献更新 - {run_date}"


def run_literature_monitor(config_path: str | Path, *, days: int | None = None, dry_run: bool | None = None) -> ReportResult:
    config = load_config(config_path)
    if dry_run is not None:
        config.setdefault("safety", {})["dry_run"] = dry_run
    schedule = config.get("schedule", {})
    default_days = int(days or schedule.get("default_days", 7))
    fallback_days = int(schedule.get("fallback_days", 30))
    min_strong = int(schedule.get("min_strong_results", 2))

    candidates = _collect_candidates(config, default_days)
    candidates = _verify_candidates(candidates, config, default_days)
    candidates = rank_candidates(deduplicate_candidates(candidates))
    fallback_used = False

    if _count_strong(candidates) < min_strong and fallback_days > default_days and days is None:
        fallback_used = True
        more = _collect_candidates(config, fallback_days)
        more = _verify_candidates(more, config, fallback_days)
        candidates = rank_candidates(deduplicate_candidates(candidates + more))
        used_days = fallback_days
    else:
        used_days = default_days

    included, excluded = split_included_excluded(candidates, config)
    run_date = date.today().isoformat()
    subject = _subject(config, run_date)
    body = _build_email_with_llm(config, included, excluded, used_days, fallback_used)
    report = ReportResult(run_date=run_date, search_window_days=used_days, fallback_used=fallback_used, included=included, excluded=excluded, subject=subject, body_markdown=body)

    output_root = config.get("outputs", {}).get("dir", "outputs")
    run_dir = write_run_outputs(report, candidates, output_root)
    LOGGER.info("Wrote outputs to %s", run_dir)

    if config.get("state", {}).get("enabled", True):
        HistoryStore(config.get("state", {}).get("path", "data/history.json")).load().update(included)
        store = HistoryStore(config.get("state", {}).get("path", "data/history.json")).load()
        store.update(included)
        store.save()

    email_enabled = bool(config.get("email", {}).get("enabled", False))
    is_dry_run = bool(config.get("safety", {}).get("dry_run", True))
    if email_enabled and not is_dry_run:
        mode = config.get("email", {}).get("mode", "smtp")
        if mode == "gmail_api":
            send_gmail_api_email(config, subject, body)
        else:
            send_smtp_email(config, subject, body)
    return report

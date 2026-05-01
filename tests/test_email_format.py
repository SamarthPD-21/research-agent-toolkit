from research_agent_toolkit.workflows.literature_monitor import _fallback_email_body


def test_email_has_required_sections():
    body = _fallback_email_body([], [], 7, False)
    required = [
        "一、本周期最重要结论",
        "二、MRI-to-PET / Tau PET / Alzheimer's disease 强相关论文",
        "三、医学图像大模型 / 医学视觉语言模型更新",
        "四、间接相关但可能有启发的论文或模型",
        "五、未纳入内容与原因",
        "六、下周建议关注关键词",
    ]
    for section in required:
        assert section in body

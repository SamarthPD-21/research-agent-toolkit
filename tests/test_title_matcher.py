from research_agent_toolkit.verification.title_matcher import normalize_title, titles_match


def test_normalize_title():
    assert normalize_title("MRI-to-PET: A Study!") == "mri to pet a study"


def test_titles_match_subtitle():
    assert titles_match("MRI-to-PET synthesis for Alzheimer's disease", "MRI-to-PET Synthesis for Alzheimer's Disease | arXiv")


def test_titles_do_not_match():
    assert not titles_match("MRI-to-PET synthesis", "A completely unrelated paper")

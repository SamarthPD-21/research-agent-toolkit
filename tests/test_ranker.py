from research_agent_toolkit.processing.ranker import rank_candidate
from research_agent_toolkit.schemas import CandidateItem


def test_rank_score_range():
    item = CandidateItem(
        id="1",
        module="neuro_pet",
        item_type="paper",
        title="MRI-to-PET synthesis for Alzheimer's disease using multimodal deep learning",
        source="arXiv",
        url="https://arxiv.org/abs/1",
        abstract="PET MRI tau amyloid FDG reconstruction code GitHub",
    )
    ranked = rank_candidate(item)
    assert 0 <= ranked.scores.priority <= 100
    assert ranked.scores.relevance > 0

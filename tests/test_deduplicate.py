from research_agent_toolkit.processing.deduplicate import deduplicate_candidates
from research_agent_toolkit.schemas import CandidateItem


def test_deduplicate_by_doi():
    a = CandidateItem(id="1", module="neuro_pet", item_type="paper", title="A", source="arXiv", url="https://a", doi="10.1/a")
    b = CandidateItem(id="2", module="neuro_pet", item_type="paper", title="A formal", source="PubMed", url="https://b", doi="10.1/a")
    out = deduplicate_candidates([a, b])
    assert len(out) == 1
    assert out[0].source == "PubMed"


def test_deduplicate_by_title():
    a = CandidateItem(id="1", module="medical_vlm", item_type="paper", title="Medical CLIP for Radiology", source="arXiv", url="https://a")
    b = CandidateItem(id="2", module="medical_vlm", item_type="paper", title="Medical-CLIP for radiology", source="Crossref", url="https://b")
    out = deduplicate_candidates([a, b])
    assert len(out) == 1

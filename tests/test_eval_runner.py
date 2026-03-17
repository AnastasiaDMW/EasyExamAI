import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evals.eval_runner import (
    eval_routing,
    eval_retrieval,
    eval_latency,
    eval_end_to_end
)

class FakeLLM:
    def invoke(self, prompt: str) -> str:
        prompt = prompt.lower()

        if "generate" in prompt or "test" in prompt:
            return "TEST"

        return "TUTOR"


class FakeDoc:
    def __init__(self, text):
        self.page_content = text


@pytest.fixture(autouse=True)
def mock_everything(monkeypatch):
    fake_llm = FakeLLM()

    import llm.llm_model as llm_module
    import agents.orchestrator_agent as orchestrator_module
    import skills.explain_topic as explain_module
    import skills.generate_test as generate_module
    import skills.process_document as process_module

    monkeypatch.setattr(llm_module, "llm", fake_llm)
    monkeypatch.setattr(orchestrator_module, "llm", fake_llm)
    monkeypatch.setattr(explain_module, "llm", fake_llm)
    monkeypatch.setattr(generate_module, "llm", fake_llm)
    monkeypatch.setattr(process_module, "llm", fake_llm)

    import skills.semantic_search as search_module

    def fake_retrieve(query: str):
        return [FakeDoc(f"This text contains {query}")]

    def fake_semantic_search(query: str):
        return f"context about {query}"

    monkeypatch.setattr(search_module, "retrieve_documents", fake_retrieve)
    monkeypatch.setattr(search_module, "semantic_search", fake_semantic_search)


def test_routing():
    accuracy = eval_routing()
    assert accuracy >= 0.5


def test_retrieval():
    score = eval_retrieval()
    assert score >= 0.5


def test_latency():
    avg_latency = eval_latency()
    assert avg_latency < 5


def test_end_to_end():
    eval_end_to_end()
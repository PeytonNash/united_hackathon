from fastapi.testclient import TestClient
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import services.cost_evaluator.main as ce 
import pytest


# Stub for Gemini response
class DummyResponse:
    text = "[0.8, 0.6]"  # The mock output of the model

# Automatically patch Gemini during all tests
@pytest.fixture(autouse=True)
def patch_gemini(monkeypatch):
    import services.cost_evaluator.main as ce_mod
    monkeypatch.setattr(
        ce_mod.model, 
        "generate_content", 
        lambda prompt: DummyResponse()
    )


client = TestClient(ce.app)


def test_score_options_order():
    options = [{"id": "A"}, {"id": "B"}]
    resp = client.post("/score_options", json={"options": options, "priority_score": 0.5})
    assert resp.status_code == 200
    scored = resp.json()
    assert scored[0]["score"] == 0.8
    assert scored[1]["score"] == 0.6

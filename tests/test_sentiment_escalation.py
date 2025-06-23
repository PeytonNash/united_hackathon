from fastapi.testclient import TestClient
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import services.sentiment_escalation.main as se
import pytest
import json

@pytest.fixture(autouse=True)
def patch_deps(monkeypatch):
    # Stub Gemini GenerativeModel and generate_content
    class DummyResponse:
        @property
        def text(self):
            return json.dumps({"neg": 0.9})

    class DummyModel:
        def generate_content(self, prompt):
            return DummyResponse()

    monkeypatch.setattr(se, "model", DummyModel())

    # Stub HTTPX POST call
    async def fake_post(url, json):
        class FakeResponse:
            status_code = 200
        return FakeResponse()

    monkeypatch.setattr(se, "httpx", type("HTTPXStub", (), {
        "post": fake_post
    }))


client = TestClient(se.app)


def test_sentiment_escalation_high(): 
    resp = client.post("/sentiment", json={"user_msg": "bad", "priority_score": 0.9})
    data = resp.json()
    assert data["risk"] > 0.7
    assert data["channel"] == "#premier_desk"

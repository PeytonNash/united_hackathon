from fastapi.testclient import TestClient
import services.sentiment_escalation.main as se
import pytest

@pytest.fixture(autouse=True)
def patch_deps(monkeypatch):
    # Stub OpenAI ChatCompletion
    class DummyChat:
        @staticmethod
        def create(**kwargs):
            return type("ChatResponse", (), {
                "choices": [
                    type("Choice", (), {
                        "message": type("Message", (), {
                            "function_call": type("FunctionCall", (), {
                                "arguments": {"neg": 0.9}
                            })()
                        })()
                    })()
                ]
            })()

    monkeypatch.setattr(se, "openai", type("OpenAIStub", (), {
        "ChatCompletion": DummyChat
    }))

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
    resp = client.post("/sentiment",  json={"user_msg": "bad", "priority_score": 0.9})
    data = resp.json()
    assert data["risk"] > 0.7
    assert data["channel"] == "#premier_desk"
    
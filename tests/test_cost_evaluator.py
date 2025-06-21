from fastapi.testclient import TestClient
import services.cost_evaluator.main as ce
import pytest


# stub openai
class Dummy:
    @staticmethod
    def ChatCompletion_create(**kwargs):
        class C:
            choices = [type("O",(),{"message":type("M",(),{"function_call":type("F",(),{"arguments":{"scores":[0.8,0.6]}})})})]
        return C()


@pytest.fixture(autouse=True)
def patch_openai(monkeypatch):
    import services.cost_evaluator.main as ce_mod
    monkeypatch.setattr(ce_mod.openai, "ChatCompletion", type("X",(),{"create":Dummy.ChatCompletion_create}))


client = TestClient(ce.app)


def test_score_options_order():
    options = [{"id":"A"},{"id":"B"}]
    resp = client.post("/score_options", json={"options":options, "priority_score":0.5})
    scored = resp.json()
    assert scored[0]["score"] == 0.8
    assert scored[1]["score"] == 0.6


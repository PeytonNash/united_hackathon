from fastapi.testclient import TestClient
import services.delay_explainer.agent as de
import pytest


@pytest.fixture
def client():
    return TestClient(de.app)


def test_explain_mechanical():
    ctx = {"flight_ctx": {"delay_code": "MX", "dep": "SFO"}, "docs": ["foo"]}
    resp = client.post("/delay_explainer", json=ctx)

    assert resp.status_code == 200
    
    data = resp.json()

    assert "Mechanical issue" in data["explanation"]
    assert data["assets"] == []
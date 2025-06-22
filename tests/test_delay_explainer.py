from fastapi.testclient import TestClient
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import services.delay_explainer.agent as de
import pytest


@pytest.fixture
def client():
    return TestClient(de.app)


def test_explain_mechanical(client):
    ctx = {"flight_ctx": {"delay_code": "FC", "departur_iata": "SFO"}, "docs": ["foo"]}
    resp = client.post("/delay_explainer", json=ctx)

    assert resp.status_code == 200
    
    data = resp.json()

    assert "Crew scheduling conflict." in data["explanation"]
    assert data["assets"] == []
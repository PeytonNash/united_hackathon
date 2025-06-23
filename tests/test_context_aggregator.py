from fastapi.testclient import TestClient
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import services.context_aggregator.main as ca
import pytest


@pytest.fixture
def client():
    return TestClient(ca.app)


def test_get_context_returns_flight_and_docs(client):
    resp = client.get("/context/UA384")
    assert resp.status_code == 200
    body = resp.json()
    assert body["flight_ctx"]["flight_iata"] == "UA384", 'Flight fail'
    assert "docs" in body and isinstance(body["docs"], list), 'Docs fail'

    # docs_fts contains United contract of carriage, etc., so it should appear
    assert any("United Club Terms and Conditions Important:" in d for d in body["docs"]), 'Find substring fail'
    print(body['docs'])
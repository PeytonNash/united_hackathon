from fastapi.testclient import TestClient
import services.context_aggregator.main as ca
import pytest


@pytest.fixture
def client():
    return TestClient(ca.app)


def test_get_context_returns_flight_and_docs(client):
    resp = client.get("/context/UA100")
    assert resp.status_code == 200
    body = resp.json()
    assert body["flight_ctx"]["flight_id"] == "UA100"
    assert "docs" in body and isinstance(body["docs"], list)

    # docs_fts contains §259, so it should appear
    assert any("259" in d for d in body["docs"])
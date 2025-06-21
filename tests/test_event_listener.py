from fastapi.testclient import TestClient
import services.event_listener.main as el
import pytest


@pytest.fixture
def client(monkeypatch):
    # intercept forwarding
    called = {}

    async def fake_post(url, json):
        called['url'],  called['json'] = url, json

        class R:
            status_code = 200

        return R()

    monkeypatch.setattr(el,  "httpx",  type("X", (), {"post":fake_post}))
    return TestClient(el.app),  called


def test_forward_event(client):
    cli,  called = client
    resp = cli.post("/events",  json={"flight_id":"UA100", "foo":"bar"})
    assert resp.status_code == 200
    assert called['url'].endswith("/context/UA100")
    assert called['json']['foo'] == "bar"

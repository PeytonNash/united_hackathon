from fastapi.testclient import TestClient
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
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
    resp = cli.post("/events",  json={"flight_id":"UA384", "foo":"bar"})
    assert resp.status_code == 200
    assert called['url'].endswith("/context/UA384")
    assert called['json']['foo'] == "bar"

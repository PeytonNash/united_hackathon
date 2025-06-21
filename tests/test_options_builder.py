from fastapi.testclient import TestClient
import services.options_builder.main as ob

client = TestClient(ob.app)


def test_build_options():
    ctx = {"flight_ctx": {"dep": "SFO"}}
    resp = client.post("/build_options", json=ctx)
    opts = resp.json()
    assert isinstance(opts, list) and len(opts) <= 5
    for o in opts:
        assert "flight" in o and "hotel" in o and "lounge" in o
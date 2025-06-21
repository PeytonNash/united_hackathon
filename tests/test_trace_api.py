from fastapi.testclient import TestClient
import services.trace_api.main as ta

client = TestClient(ta.app)


def test_trace_write_and_read():
    payload = {"foo":"bar"}
    post = client.post("/trace", json={"payload":payload})
    tid = post.json()["trace_id"]
    get = client.get(f"/trace/{tid}")
    assert get.json() == payload

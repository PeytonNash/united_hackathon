from fastapi.testclient import TestClient
import services.rules_policy.engine as rp

client = TestClient(rp.app)


def test_rules_and_policy_ok():
    req = {
      "flight_ctx": {"flight_id": "UA100"},
      "profile": {"tier_score": 0.9, "tags": "MED_SURGERY"},
      "docs": ["§259 rules text"]
    }
    resp = client.post("/rules_policy", json=req)
    body = resp.json()

    assert body["policy_ok"] is True
    assert "baseline_offer" in body
    assert any("tier_score" in p for p in body["rule_path"])
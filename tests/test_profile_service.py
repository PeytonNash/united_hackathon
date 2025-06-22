from fastapi.testclient import TestClient
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import services.profile_service.main as ps

client = TestClient(ps.app)


def test_profile_priority():
    resp = client.get("/profile/UA100")
    body = resp.json()
    
    assert abs(body["priority_score"] - (0.6*0.9+0.4*1.0)) < 1e-6
    assert "tier_score" in body and "tags" in body
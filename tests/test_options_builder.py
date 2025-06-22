from fastapi.testclient import TestClient
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)
import services.options_builder.main as ob

client = TestClient(ob.app)


def test_flight_options():
    ctx = {"flight_ctx": {"departure_iata": "SFO", 'arrival_iata':'PDX'}}
    resp = client.post("/flight_options", json=ctx)
    opts = resp.json()
    assert isinstance(opts, list) and len(opts) <= 5
    for o in opts:
        assert "flight_iata" in o

def test_lounge_options():
    ctx = {"flight_ctx": {"departure_iata": "SFO", 'arrival_iata':'PDX'}}
    resp = client.post("/lounge_options", json=ctx)
    opts = resp.json()
    assert isinstance(opts, list)
    for o in opts:
        assert "type" in o

def test_hotel_options():
    ctx = {"flight_ctx": {"departure_iata": "SFO", 'arrival_iata':'PDX'}}
    resp = client.post("/hotel_options", json=ctx)
    opts = resp.json()
    assert isinstance(opts, list)
    for o in opts:
        assert "hotel_name" in o
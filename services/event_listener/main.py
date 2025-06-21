from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()
CTX_URL = os.getenv("CTX_AGG_URL", "http://localhost:8001/context/")


@app.post("/events")
async def on_event(req: Request):
    evt = await req.json()
    flight = evt.get("flight_id")

    # forward raw event to Context Aggregator
    if flight:
        await httpx.post(f"{CTX_URL}{flight}", json=evt)

    return {"status": "forwarded", "flight": flight}

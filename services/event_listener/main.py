from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv 

app = FastAPI()

load_dotenv()

CTX_URL = os.getenv("CTX_AGG_URL")

@app.post("/events")
async def on_event(req: Request):
    evt = await req.json()
    flight = evt.get("flight_id")

    # forward raw event to Context Aggregator
    if flight:
        await httpx.post(f"{CTX_URL}{flight}", json=evt)

    return {"status": "forwarded", "flight": flight}

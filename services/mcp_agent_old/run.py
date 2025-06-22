import asyncio
import uvicorn
from fastapi import FastAPI
from .agent import agent

app = FastAPI(title="MCP Agent Service")

@app.post("/agent/disruption")
async def disruption(payload: dict):
    flight_id = payload["flight_id"]
    pax_id    = payload["pax_id"]
    result = await agent.handle_disruption(flight_id, pax_id)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)

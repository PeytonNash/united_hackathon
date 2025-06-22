from fastapi import FastAPI
from .graph import build_agent_graph

app = FastAPI()
agent_graph = build_agent_graph()

@app.post("/agent/disruption")
async def handle_disruption(payload: dict):
    flight_id = payload["flight_id"]
    pax_id = payload["pax_id"]

    output = await agent_graph.ainvoke({
        "flight_id": flight_id,
        "pax_id": pax_id
    })

    return output

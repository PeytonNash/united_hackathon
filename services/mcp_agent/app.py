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

@app.post("/agent/followup")
async def handle_followup(payload: dict):
    user_msg = payload["user_msg"]
    flight_id = payload["flight_id"]
    pax_id = payload["pax_id"]

    # context + profile still relevant
    result = await agent_graph.ainvoke({
        "flight_id": flight_id,
        "pax_id": pax_id,
        "user_msg": user_msg,
        "followup": True
    })
    return result


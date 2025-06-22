from fastapi import FastAPI
from pydantic import BaseModel
from .graph import build_options_graph

app = FastAPI(title="Options Builder Agent")

agent = build_options_graph()

class RequestCtx(BaseModel):
    flight_ctx: dict
    rules_policy: dict  

@app.post("/agent/build_options")
async def build(req: RequestCtx):
    result = await agent.ainvoke({"flight_ctx": req.flight_ctx})
    return {"options": result}

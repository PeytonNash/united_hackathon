import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# only top 5 IATA codes
CODE_MAP = {
  "WX": "Weather at {dep} is causing delays.",
  "MX": "Mechanical issue on inbound aircraft.",
  "ATC": "Air traffic control restrictions.",
  "CREW": "Crew scheduling conflict.",
  "OPS": "Operational delay."
}

class Context(BaseModel):
    flight_ctx: dict
    docs: list[str]

@app.post("/delay_explainer")
def explain(ctx: Context):
    code = ctx.flight_ctx.get("delay_code", "")
    tpl  = CODE_MAP.get(code, "Delay cause unavailable.")
    text = tpl.format(**ctx.flight_ctx)
    assets = []
    # attach first doc if weather
    if code == "WX" and ctx.docs:
        assets.append(ctx.docs[0])
    return {"explanation": text, "assets": assets}
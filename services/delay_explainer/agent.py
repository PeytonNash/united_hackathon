import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

CODE_MAP = {
  "WO": "Weather at {departure} is causing delays.",
  "WT": "Weather at {arrival} is causing delays.",
  "WR": "Weather en route is causing delays.",
  "AT": "Air traffic control restrictions.",
  "FC": "Crew scheduling conflict.",
  "FP": "Operational delay."
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
    if code in ['WO', 'WT', 'WR'] and ctx.docs:
        assets.append(ctx.docs[0])

    return {"explanation": text, "assets": assets}

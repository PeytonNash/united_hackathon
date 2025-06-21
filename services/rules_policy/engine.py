from fastapi import FastAPI
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader
import yaml
import os

app = FastAPI()
env = Environment(loader=FileSystemLoader('infra/rules'))
rules_tmpl = env.get_template('ua_rules.yml')


class Req(BaseModel):
    flight_ctx: dict
    profile: dict
    docs: list[str]


@app.post("/rules_policy")
def rules_policy(req: Req):
    # baseline offer via YAML/Jinja
    offer = rules_tmpl.render(flight=req.flight_ctx, profile=req.profile)
    # simple DOT check
    policy_ok = any("§259" in d for d in req.docs)
    # rule_path just echoes keys used
    rule_path = [f"{k}={v}" for k,v in req.profile.items() if k in ["tier_score", "tags"]]
    return {"baseline_offer": offer, "policy_ok": policy_ok, "rule_path": rule_path}

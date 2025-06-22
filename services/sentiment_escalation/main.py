from fastapi import FastAPI
from pydantic import BaseModel
import openai
import math
import os
from dotenv import load_dotenv
import httpx

app = FastAPI()

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY") ##### NEEDS TO BE UPDATED FOR GEMINI
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")


class Req(BaseModel): 
    user_msg: str
    priority_score: float


@app.post("/sentiment")
async def sentiment(req:  Req): 
    resp = openai.ChatCompletion.create(
      model="gpt-4o", 
      messages=[{"role": "user", "content": req.user_msg}], 
      functions=[{"name": "sentiment", "parameters": {
          "type": "object", 
          "properties": {"neg": {"type": "number"}}, 
          "required": ["neg"]
      }}], 
      function_call={"name": "sentiment"}
    )

    neg = resp.choices[0].message.function_call.arguments["neg"]
    risk = 1/(1+math.exp(- (1.5*neg + req.priority_score)))
    channel = "#premier_desk" if risk > 0.7 else "#ops_general"

    # post to Slack if high-risk
    if risk > 0.7:
        await httpx.post(SLACK_WEBHOOK,  json={"text": f"Escalation risk {risk: .2f}"})

    return {"risk":  risk,  "channel":  channel}

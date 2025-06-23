from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import math
import os
from dotenv import load_dotenv
import httpx

app = FastAPI()

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")


class Req(BaseModel): 
    user_msg: str
    priority_score: float

model = genai.GenerativeModel('gemini-2.5-pro')

@app.post("/sentiment")
async def sentiment(req: Req):
    prompt = f"""
    You are a sentiment analysis function. The user message is:
    "{req.user_msg}"

    Return a JSON object with a single key "neg" representing how negative the message is (0 = not negative, 1 = very negative).
    Only return JSON.
    """

    response = model.generate_content(prompt)
    
    # Extract JSON from the response text
    import json
    try:
        neg_data = json.loads(response.text)
        neg = float(neg_data["neg"])
    except Exception as e:
        raise ValueError(f"Failed to parse Gemini response: {response.text}") from e

    risk = 1 / (1 + math.exp(-(1.5 * neg + req.priority_score)))
    channel = "#premier_desk" if risk > 0.7 else "#ops_general"

    if risk > 0.7:
        await httpx.post(SLACK_WEBHOOK, json={"text": f"Escalation risk {risk:.2f}"})

    return {"risk": risk, "channel": channel}
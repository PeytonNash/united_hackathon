from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_KEY")


class Req(BaseModel): 
    options: list[dict]
    priority_score: float


@app.post("/score_options")
def score_options(req: Req):
    resp = openai.ChatCompletion.create(
      model="gpt-4o", 
      messages=[{"role": "user", "content": "Score these options."}], 
      functions=[{
        "name": "rate", 
        "parameters": {
          "type": "object", 
          "properties": {
            "scores": {"type": "array", "items": {"type": "number"}}
          }, 
          "required": ["scores"]
        }
      }], 
      function_call={"name": "rate"}, 
      arguments={"options": req.options,  "priority": req.priority_score}
    )
    scores = resp.choices[0].message.function_call.arguments.get("scores", [])

    # attach & sort
    for opt,  s in zip(req.options,  scores): 
        opt["score"] = s
    return sorted(req.options, key=lambda o: o["score"], reverse=True)
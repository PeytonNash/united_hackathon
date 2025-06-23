from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Authenticate with Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Set GEMINI_API_KEY in your environment

# Gemini model instance
model = genai.GenerativeModel("gemini-2.5-pro")


class Req(BaseModel): 
    options: list[dict]
    priority_score: float


@app.post("/score_options")
def score_options(req: Req):
    prompt = (
        "Given a list of options and a priority score, assign a numeric score (0 to 1) to each option. "
        "Return a list of scores in the same order.\n\n"
        f"Priority score: {req.priority_score}\n\n"
        f"Options: {req.options}\n\n"
        "Respond only with a JSON array of numbers like: [0.6, 0.2, 0.9]"
    )

    response = model.generate_content(prompt)
    
    # Parse the response
    import json, re
    match = re.search(r"\[.*?\]", response.text)
    scores = json.loads(match.group()) if match else [0.0 for _ in req.options]

    # Attach scores to options
    for opt, s in zip(req.options, scores): 
        opt["score"] = s
    return sorted(req.options, key=lambda o: o["score"], reverse=True)

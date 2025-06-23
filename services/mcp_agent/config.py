from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "http://localhost:8000"

ENDPOINTS = {
    "context": "/context/{flight_id}",
    "delay_explainer": "/delay_explainer",
    "profile": "/profile/{pax_id}",
    "rules_policy": "/rules_policy",
    "build_options_agent": "/agent/build_options",
    "score_options": "/score_options",
    "sentiment": "/sentiment",
    "trace": "/trace",
}

GCP_PROJECT_ID = os.getenv("BQ_PROJECT")
VERTEX_MODEL = "gemini-1.5-flash"

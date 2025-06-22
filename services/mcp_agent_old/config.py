BASE_URL = "http://localhost:8000" 

ENDPOINTS = {
    "context": "/context/{flight_id}",
    "delay_explainer": "/delay_explainer",
    "profile": "/profile/{pax_id}",
    "rules_policy": "/rules_policy",
    "build_options": "/build_options",
    "score_options": "/score_options",
    "sentiment": "/sentiment",
    "trace": "/trace",
}

GEMINI_MODEL = "gemini-1.5-flash-001"
GEMINI_KEY = "<our-key>"


from langchain.tools import tool
import httpx
from .config import BASE_URL, ENDPOINTS

client = httpx.AsyncClient(base_url=BASE_URL, timeout=10)

@tool
async def get_context(flight_id: str) -> dict:
    """Fetch structured/unstructured context for a flight"""
    r = await client.get(ENDPOINTS["context"].format(flight_id=flight_id))
    return r.json()

@tool
async def get_profile(pax_id: str) -> dict:
    """Get customer profile by ID"""
    r = await client.get(ENDPOINTS["profile"].format(pax_id=pax_id))
    return r.json()

@tool
async def explain_delay(flight_ctx: dict) -> dict:
    """Generate a human-readable delay explanation"""
    r = await client.post(ENDPOINTS["delay_explainer"], json={"flight_ctx": flight_ctx})
    return r.json()

@tool
async def apply_rules(flight_ctx: dict, profile: dict, docs: list[str] = []) -> dict:
    """Apply rules based on customer and flight context"""
    payload = {"flight_ctx": flight_ctx, "profile": profile, "docs": docs}
    r = await client.post(ENDPOINTS["rules_policy"], json=payload)
    return r.json()

@tool
async def build_options(flight_ctx: dict) -> list:
    """Get alternate flights/hotels/lounges given flight context"""
    r = await client.post(ENDPOINTS["build_options"], json={"flight_ctx": flight_ctx})
    return r.json()

@tool
async def score_options(options: list, priority_score: float) -> list:
    """Score alternate options based on customer priority"""
    r = await client.post(ENDPOINTS["score_options"], json={"options": options, "priority_score": priority_score})
    return r.json()

@tool
async def post_trace(trace_payload: dict) -> str:
    """Log agent decisions and return trace ID"""
    r = await client.post(ENDPOINTS["trace"], json=trace_payload)
    return r.json().get("trace_id")

@tool
async def analyze_sentiment(text: str, priority_score: float) -> dict:
    """Analyze sentiment and compute escalation risk."""
    r = await client.post(ENDPOINTS["sentiment"], json={"user_msg": text, "priority_score": priority_score})
    return r.json()

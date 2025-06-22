import os
import httpx
from .config import BASE_URL, ENDPOINTS

client = httpx.AsyncClient(base_url=BASE_URL, timeout=10.0)

async def get_context(flight_id: str) -> dict:
    r = await client.get(ENDPOINTS["context"].format(flight_id=flight_id))
    r.raise_for_status()
    return r.json()

async def explain_delay(flight_ctx: dict) -> dict:
    r = await client.post(ENDPOINTS["delay_explainer"], json={"flight_ctx": flight_ctx})
    r.raise_for_status()
    return r.json()

async def get_profile(pax_id: str) -> dict:
    r = await client.get(ENDPOINTS["profile"].format(pax_id=pax_id))
    r.raise_for_status()
    return r.json()

async def apply_rules(flight_ctx: dict, profile: dict, docs: list[str] = None) -> dict:
    payload = {"flight_ctx": flight_ctx, "profile": profile, "docs": docs or []}
    r = await client.post(ENDPOINTS["rules_policy"], json=payload)
    r.raise_for_status()
    return r.json()

async def build_options(flight_ctx: dict, baseline_offer: dict) -> list:
    payload = {"flight_ctx": flight_ctx, "baseline_offer": baseline_offer}
    r = await client.post(ENDPOINTS["build_options"], json=payload)
    r.raise_for_status()
    return r.json()

async def score_options(options: list, priority_score: float) -> list:
    payload = {"options": options, "priority_score": priority_score}
    r = await client.post(ENDPOINTS["score_options"], json=payload)
    r.raise_for_status()
    return r.json()

async def analyze_sentiment(text: str, priority_score: float) -> dict:
    payload = {"user_msg": text, "priority_score": priority_score}
    r = await client.post(ENDPOINTS["sentiment"], json=payload)
    r.raise_for_status()
    return r.json()

async def post_trace(trace_payload: dict) -> str:
    r = await client.post(ENDPOINTS["trace"], json=trace_payload)
    r.raise_for_status()
    return r.json().get("trace_id")

import asyncio
from .tools import (
    get_context, explain_delay, get_profile, apply_rules,
    build_options, score_options, analyze_sentiment, post_trace
)

class MCPAgent:
    """Central orchestrator agent."""
    async def handle_disruption(self, flight_id: str, pax_id: str):
        # context
        ctx = await get_context(flight_id)

        # delay explanation, profile, rules
        delay_task = explain_delay(ctx["flight_ctx"])
        profile_task = get_profile(pax_id)
        # wait for profile first to pass into rules
        explanation, profile = await asyncio.gather(delay_task, profile_task)

        rules = await apply_rules(ctx["flight_ctx"], profile)

        # options
        options = await build_options(ctx["flight_ctx"], rules["baseline_offer"])

        # scoring
        scored = await score_options(options, profile["priority_score"])

        # sentiment (kick off but don't block UI)
        sentiment = await analyze_sentiment(
            text=explanation.get("explanation", ""), 
            priority_score=profile["priority_score"]
        )

        # trace
        trace_payload = {
            "flight_id": flight_id,
            "pax_id": pax_id,
            "delay_explanation": explanation,
            "profile": profile,
            "rules_policy": rules,
            "options": scored,
            "sentiment": sentiment,
        }
        trace_id = await post_trace(trace_payload)

        return {
            "options": scored,
            "trace_id": trace_id
        }

agent = MCPAgent()

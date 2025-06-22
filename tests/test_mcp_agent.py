import pytest
import asyncio

from services.mcp_agent_old.agent import MCPAgent

class DummyTools:
    """Monkey-patched tools returning fixed data."""
    @staticmethod
    async def get_context(flight_id): 
        return {"flight_ctx": {"flight_id": flight_id}}
    @staticmethod
    async def explain_delay(ctx): 
        return {"explanation": f"delay for {ctx['flight_id']}"}
    @staticmethod
    async def get_profile(pax_id): 
        return {"priority_score": 0.5}
    @staticmethod
    async def apply_rules(ctx, prof): 
        return {"baseline_offer": {"offer": "ok"}}
    @staticmethod
    async def build_options(ctx, base): 
        return [{"opt": 1}, {"opt": 2}]
    @staticmethod
    async def score_options(opts, score): 
        # reverse order to test sorting
        return sorted(opts, key=lambda x: -x["opt"])
    @staticmethod
    async def analyze_sentiment(text, priority_score): 
        return {"risk": 0.2}
    @staticmethod
    async def post_trace(payload): 
        return "TRACE123"

@pytest.fixture(autouse=True)
def patch_tools(monkeypatch):
    import services.mcp_agent_old.tools as tools
    for name in [
        "get_context","explain_delay","get_profile","apply_rules",
        "build_options","score_options","analyze_sentiment","post_trace"
    ]:
        monkeypatch.setattr(tools, name, getattr(DummyTools, name))

def test_handle_disruption():
    agent = MCPAgent()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(agent.handle_disruption("F1", "P1"))
    assert "options" in result
    assert result["trace_id"] == "TRACE123"
    assert isinstance(result["options"], list)

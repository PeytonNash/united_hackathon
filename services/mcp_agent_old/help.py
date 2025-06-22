from langchain.agents import Tool
 
TOOLS = [
    Tool(
        name="get_context",
        func=lambda flight_iata: requests.get(f"http://localhost:8001/context/{flight_iata}").text,
        description="Fetch flight context and docs JSON for a given flight IATA code"
    ),
    Tool(
        name="explain_delay",
        func=lambda ctx_json: requests.post("http://localhost:8002/delay_explainer", json=ctx_json).text,
        description="Explain why the flight was delayed, given the context JSON"
    ),
    Tool(
        name="get_profile",
        func=lambda customer_id: requests.get(f"http://localhost:8004/profile/{customer_id}").text,
        description="Fetch customer profile JSON by customer ID"
    ),
    Tool(
        name="apply_rules",
        func=lambda payload_json: requests.post("http://localhost:8003/rules_policy", json=payload_json).text,
        description="Apply rebooking rules given flight context, profile, and docs"
    ),
    Tool(
        name="build_options",
        func=lambda ctx_json: requests.post("http://localhost:8005/build_options", json={"flight_ctx": ctx_json["flight_ctx"]}).text,
        description="Generate up to 5 rebooking options given flight context"
    ),
    Tool(
        name="score_options",
        func=lambda payload_json: requests.post("http://localhost:8006/score_options", json=payload_json).text,
        description="Rank options JSON by customer priority and cost function"
    ),
    Tool(
        name="analyze_sentiment",
        func=lambda payload_json: requests.post("http://localhost:8007/sentiment", json=payload_json).text,
        description="Compute escalation risk and channel based on sentiment and profile"
    ),
    Tool(
        name="record_trace",
        func=lambda payload_json: requests.post("http://localhost:8008/trace", json={"payload": payload_json}).text,
        description="Record the full decision trace and return a trace ID"
    ),
]
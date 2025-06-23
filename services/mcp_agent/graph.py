from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from .tools import get_context, get_profile, explain_delay, apply_rules, delegate_options_builder, analyze_sentiment, score_options, post_trace
from .reasoning import chain as llm

def dispatch_tool(output):
    return output.get("tool_name")

def build_agent_graph():
    builder = StateGraph(state_schema={"user_query": str})

    builder.set_entry_point("context")
    builder.set_entry_point("think")
    builder.add_node("context", get_context)
    builder.add_node("profile", get_profile)
    builder.add_node("explanation", explain_delay)
    builder.add_node("rules", apply_rules)
    
    # hand off to options builder agent
    builder.add_node("options", delegate_options_builder)

    builder.add_node("score", score_options)
    builder.add_node("sentiment", analyze_sentiment)
    builder.add_node("trace", post_trace)
    
    # we don't use this yet but maybe for future
    builder.add_node("decide", llm.bind_tools([
        get_context, get_profile, explain_delay, apply_rules, score_options, analyze_sentiment, post_trace
    ]))

    # use this when nthe user follows up
    builder.add_node("think", llm.bind_tools([
        explain_delay,
        delegate_options_builder
    ]))

    builder.add_conditional_edges(
        "think",
        dispatch_tool,
        {
            "explain_delay": "explanation",
            "delegate_options_builder": "options",
            "end": END
        }
    )

    # linear path for now
    builder.connect("context", "profile")
    builder.connect("profile", "explanation")
    builder.connect("explanation", "rules")
    builder.connect("rules", "options")
    builder.connect("options", "score")
    builder.connect("score", "sentiment")
    builder.connect("sentiment", "trace")
    builder.connect("trace", END)

    return builder.compile()

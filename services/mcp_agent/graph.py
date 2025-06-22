from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from .tools import get_context, get_profile, explain_delay, apply_rules, build_options, score_options, post_trace
from .reasoning import llm

def build_agent_graph():
    builder = StateGraph()

    builder.set_entry_point("context")
    builder.add_node("context", get_context)
    builder.add_node("profile", get_profile)
    builder.add_node("explanation", explain_delay)
    builder.add_node("rules", apply_rules)
    builder.add_node("options", build_options)
    builder.add_node("score", score_options)
    builder.add_node("trace", post_trace)
    
    builder.add_node("decide", llm.bind_tools([
        get_context, get_profile, explain_delay, apply_rules, build_options, score_options, post_trace
    ]))

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

from langgraph.graph import StateGraph, END
from .tools import flight_options, hotel_options, lounge_options
from .reasoning import chain as llm

def build_options_graph():
    g = StateGraph()

    # instead of hardcoding the sequence of tools
    think_node = llm.bind_tools([
        flight_options,
        hotel_options,
        lounge_options
    ])

    g.set_entry_point("think")
    g.add_node("think", think_node)
    g.add_edge("think", END)

    return g.compile()

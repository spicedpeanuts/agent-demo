from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import planner_node, tool_node

graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("tool", tool_node)

graph.set_entry_point("planner")

graph.add_conditional_edges(
    "planner",
    lambda s: s["next_action"],
    {
        "get_weather": "tool",
        "finish": "__end__",
    }
)

graph.add_edge("tool", "planner")

app = graph.compile()


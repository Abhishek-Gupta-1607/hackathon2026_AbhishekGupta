from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.nodes import decide_action, execute_route

def build_graph():
    """Compiles the custom StateGraph for the support agent."""
    graph_builder = StateGraph(AgentState)
    
    # Add our nodes
    graph_builder.add_node("decide_action", decide_action)
    graph_builder.add_node("execute_route", execute_route)
    
    # Define exact edges (linear pipeline)
    # Ticket -> LLM Decision -> Execute Action -> End
    graph_builder.add_edge(START, "decide_action")
    graph_builder.add_edge("decide_action", "execute_route")
    graph_builder.add_edge("execute_route", END)
    
    return graph_builder.compile()

# Build the singleton graph
support_graph = build_graph()

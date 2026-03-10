from langgraph.graph import StateGraph, END
from agent.state import AgentState

from agent.nodes.retrieve import retrieve_node
from agent.nodes.prompt import build_prompt_node
from agent.nodes.llm import llm_node
from agent.nodes.memory import memory_node


def build_graph(db, llm):

    workflow = StateGraph(AgentState)

    # nodes
    workflow.add_node("retrieve", lambda s: retrieve_node(s, db))
    workflow.add_node("prompt", build_prompt_node)
    workflow.add_node("llm", lambda s: llm_node(s, llm))
    workflow.add_node("memory", memory_node)

    # entry point
    workflow.set_entry_point("retrieve")

    # edges
    workflow.add_edge("retrieve", "prompt")
    workflow.add_edge("prompt", "llm")
    workflow.add_edge("llm", "memory")
    workflow.add_edge("memory", END)

    return workflow.compile()
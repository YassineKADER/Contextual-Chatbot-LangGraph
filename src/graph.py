from typing import List, Dict, TypedDict
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from config import llm_gemini  # Import from config
from langgraph.graph import StateGraph, END
from data_handler import retrieve_data


# Define state type
class GraphStateDict(TypedDict):
    query: str
    retrieved_data: List[str]
    initial_response: str
    refinement: str
    chat_history: List[Dict]
    output: str
    steps: List[str]
    next: str


# Nodes
def input_node(state: GraphStateDict) -> GraphStateDict:
    state["steps"].append("input node")
    return state


def retrieve_node(state: GraphStateDict) -> GraphStateDict:
    state["retrieved_data"] = retrieve_data(state["query"])
    state["steps"].append("retrieval node")
    return state


def llm_node(state: GraphStateDict) -> GraphStateDict:
    messages = [
        SystemMessage(
            content="""You are an expert chatbot, your job is to provide a comprehensive response based on the context provided.
            If you do not know the answer just say 'I do not have enough information to answer your query, please contact an agent'"""
        ),
        HumanMessage(
            content=f"Context : {state['retrieved_data']}\n Query : {state['query']}"
        ),
    ]

    state["initial_response"] = llm_gemini.invoke(messages).content
    state["steps"].append("llm node")
    return state


def decision_node(state: GraphStateDict) -> GraphStateDict:
    if (
        "I do not have enough information to answer your query, please contact an agent"
        in state["initial_response"]
    ):
        state["next"] = "final_output"
    else:
        state["next"] = "refine"
    return state


def refine_node(state: GraphStateDict) -> GraphStateDict:
    messages = [
        SystemMessage(
            content="""You are an expert chatbot, your job is to provide a comprehensive response based on the context provided.
        If you do not know the answer just say 'I do not have enough information to answer your query, please contact an agent'"""
        ),
        HumanMessage(
            content=f"""Context : {state['retrieved_data']}\n Query : {state['query']} \n Initial Response: {state['initial_response']} \n Refine the initial response by providing more information and ensuring that it provides a complete answer"""
        ),
    ]
    state["refinement"] = llm_gemini.invoke(messages).content
    state["steps"].append("refine node")
    return state


def final_output_node(state: GraphStateDict) -> GraphStateDict:
    state["output"] = (
        state["refinement"] if state["refinement"] else state["initial_response"]
    )
    state["steps"].append("final_output_node")
    return state


# Graph Setup
def get_next(state: GraphStateDict) -> str:
    return state["next"]


# Initialize graph
graph = StateGraph(GraphStateDict)

# Add nodes
graph.add_node("input", input_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("llm", llm_node)
graph.add_node("decision", decision_node)
graph.add_node("refine", refine_node)
graph.add_node("final_output", final_output_node)

# Configure edges
graph.set_entry_point("input")
graph.add_edge("input", "retrieve")
graph.add_edge("retrieve", "llm")
graph.add_edge("llm", "decision")
graph.add_conditional_edges("decision", get_next)
graph.add_edge("refine", "final_output")
graph.add_edge("final_output", END)

app = graph.compile()

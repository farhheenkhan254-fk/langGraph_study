from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    topic: str
    contributions: Annotated[list[str], operator.add]

def researcher(state: State):
    return {"contributions": [f"Researcher: key facts about {state['topic']}"]}

def reviewer(state: State):
    return {"contributions": [f"Reviewer: check accuracy and clarity for {state['topic']}"]}

def writer(state: State):
    return {"contributions": [f"Writer: combine findings into a short explanation of {state['topic']}"]}

builder = StateGraph(State)
builder.add_node("researcher", researcher)
builder.add_node("reviewer", reviewer)
builder.add_node("writer", writer)
builder.add_edge(START, "researcher")
builder.add_edge("researcher", "reviewer")
builder.add_edge("reviewer", "writer")
builder.add_edge("writer", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"topic": "GraphRAG", "contributions": []}))

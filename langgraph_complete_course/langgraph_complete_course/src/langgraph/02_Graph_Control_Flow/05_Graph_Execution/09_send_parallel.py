from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

class State(TypedDict):
    topics: list[str]
    results: Annotated[list[str], operator.add]

class WorkerState(TypedDict):
    topic: str
    results: Annotated[list[str], operator.add]

def dispatch(state: State):
    return [Send("research", {"topic": topic, "results": []}) for topic in state["topics"]]

def research(state: WorkerState):
    return {"results": [f"Research completed: {state['topic']}"]}

builder = StateGraph(State)
builder.add_node("research", research)
builder.add_conditional_edges(START, dispatch)
builder.add_edge("research", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"topics": ["RDF", "OWL", "SPARQL"], "results": []}))

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message: str

def greet(state: State):
    return {"message": state["message"] + " LangGraph!"}

builder = StateGraph(State)
builder.add_node("greet", greet)
builder.add_edge(START, "greet")
builder.add_edge("greet", END)
graph = builder.compile()

if __name__ == "__main__":
    print(graph.invoke({"message": "Hello"}))

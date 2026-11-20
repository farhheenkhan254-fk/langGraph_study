from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class WorkflowState(TypedDict):
    name: str
    greeting: str

def make_greeting(state: WorkflowState):
    return {"greeting": f"Welcome, {state['name']}!"}

builder = StateGraph(WorkflowState)
builder.add_node("make_greeting", make_greeting)
builder.add_edge(START, "make_greeting")
builder.add_edge("make_greeting", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"name": "Student", "greeting": ""}))

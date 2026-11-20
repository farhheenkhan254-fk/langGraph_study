from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    result: str

def task(state: State):
    return {"result": "Workflow started, task executed, and workflow ended."}

builder = StateGraph(State)
builder.add_node("task", task)
builder.add_edge(START, "task")
builder.add_edge("task", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"result": ""}))

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    count: int
    log: list[str]

def increment(state: State):
    new_count = state["count"] + 1
    return {"count": new_count, "log": state["log"] + [f"Count = {new_count}"]}

def continue_loop(state: State):
    return "again" if state["count"] < 3 else "finish"

builder = StateGraph(State)
builder.add_node("increment", increment)
builder.add_edge(START, "increment")
builder.add_conditional_edges("increment", continue_loop, {"again": "increment", "finish": END})
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"count": 0, "log": []}))

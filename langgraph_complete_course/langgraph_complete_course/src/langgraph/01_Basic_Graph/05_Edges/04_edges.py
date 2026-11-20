from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    steps: list[str]

def step_one(state: State):
    return {"steps": state["steps"] + ["step 1 completed"]}

def step_two(state: State):
    return {"steps": state["steps"] + ["step 2 completed"]}

builder = StateGraph(State)
builder.add_node("one", step_one)
builder.add_node("two", step_two)
builder.add_edge(START, "one")
builder.add_edge("one", "two")
builder.add_edge("two", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"steps": []}))

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    score: int
    result: str

def evaluate(state: State):
    return {"result": "pending"}

def choose_path(state: State) -> Literal["pass", "retry"]:
    return "pass" if state["score"] >= 50 else "retry"

def passed(state: State):
    return {"result": "Passed"}

def retry(state: State):
    return {"result": "Needs improvement"}

builder = StateGraph(State)
builder.add_node("evaluate", evaluate)
builder.add_node("passed", passed)
builder.add_node("retry", retry)
builder.add_edge(START, "evaluate")
builder.add_conditional_edges("evaluate", choose_path, {"pass": "passed", "retry": "retry"})
builder.add_edge("passed", END)
builder.add_edge("retry", END)
app = builder.compile()

if __name__ == "__main__":
    print("Score 72:", app.invoke({"score": 72, "result": ""}))
    print("Score 35:", app.invoke({"score": 35, "result": ""}))

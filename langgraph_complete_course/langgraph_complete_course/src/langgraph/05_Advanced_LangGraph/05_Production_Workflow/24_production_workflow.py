from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    request: str
    validated: bool
    output: str
    error: str

def validate(state: State):
    ok = bool(state["request"].strip())
    return {"validated": ok, "error": "" if ok else "Request cannot be empty."}

def route(state: State) -> Literal["process", "fail"]:
    return "process" if state["validated"] else "fail"

def process(state: State):
    return {"output": f"Processed request: {state['request']}"}

def fail(state: State):
    return {"output": "Request rejected.", "error": state["error"]}

builder = StateGraph(State)
builder.add_node("validate", validate)
builder.add_node("process", process)
builder.add_node("fail", fail)
builder.add_edge(START, "validate")
builder.add_conditional_edges("validate", route, {"process": "process", "fail": "fail"})
builder.add_edge("process", END)
builder.add_edge("fail", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"request": "Generate a course outline", "validated": False, "output": "", "error": ""}))
    print(app.invoke({"request": "   ", "validated": False, "output": "", "error": ""}))

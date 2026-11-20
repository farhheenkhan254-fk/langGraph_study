from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    request: str
    decision: str
    response: str

def decide(state: State):
    decision = "calculator" if any(ch.isdigit() for ch in state["request"]) else "general"
    return {"decision": decision}

def route(state: State) -> Literal["calculator", "general"]:
    return state["decision"]

def calculator(state: State):
    return {"response": "A number was detected. For safety, enter a clear arithmetic expression."}

def general(state: State):
    return {"response": f"You asked: {state['request']}"}

builder = StateGraph(State)
builder.add_node("decide", decide)
builder.add_node("calculator", calculator)
builder.add_node("general", general)
builder.add_edge(START, "decide")
builder.add_conditional_edges("decide", route, {"calculator": "calculator", "general": "general"})
builder.add_edge("calculator", END)
builder.add_edge("general", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"request": "What is LangGraph?", "decision": "", "response": ""}))

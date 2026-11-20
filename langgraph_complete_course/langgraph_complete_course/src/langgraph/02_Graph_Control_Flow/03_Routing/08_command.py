from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class State(TypedDict):
    question: str
    answer: str

def router(state: State) -> Command[Literal["billing", "support"]]:
    if "bill" in state["question"].lower() or "payment" in state["question"].lower():
        return Command(goto="billing")
    return Command(goto="support")

def billing(state: State):
    return {"answer": "Billing team: check your invoice and payment status."}

def support(state: State):
    return {"answer": "Support team: let's troubleshoot your issue."}

builder = StateGraph(State)
builder.add_node("router", router)
builder.add_node("billing", billing)
builder.add_node("support", support)
builder.add_edge(START, "router")
builder.add_edge("billing", END)
builder.add_edge("support", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"question": "I have a payment issue", "answer": ""}))
    print(app.invoke({"question": "My app is not opening", "answer": ""}))

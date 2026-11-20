from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

class State(TypedDict):
    draft: str
    approved: bool
    status: str

def approval_step(state: State):
    decision = interrupt({"question": "Approve this draft?", "draft": state["draft"]})
    return {"approved": bool(decision), "status": "Approved" if decision else "Rejected"}

builder = StateGraph(State)
builder.add_node("approval", approval_step)
builder.add_edge(START, "approval")
builder.add_edge("approval", END)
app = builder.compile(checkpointer=InMemorySaver())

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "approval-1"}}
    first = app.invoke({"draft": "Example proposal", "approved": False, "status": "Waiting"}, config)
    print("Paused for human decision:", first)
    answer = input("Approve? (y/n): ").strip().lower() == "y"
    print("Resumed:", app.invoke(Command(resume=answer), config))

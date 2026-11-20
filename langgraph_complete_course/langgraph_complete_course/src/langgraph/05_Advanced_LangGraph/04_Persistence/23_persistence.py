from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    notes: list[str]

def add_note(state: State):
    return {"notes": state["notes"] + ["A checkpoint was created after this node."]}

builder = StateGraph(State)
builder.add_node("add_note", add_note)
builder.add_edge(START, "add_note")
builder.add_edge("add_note", END)
saver = InMemorySaver()
app = builder.compile(checkpointer=saver)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "persistent-demo"}}
    print("Run:", app.invoke({"notes": []}, config))
    print("History:")
    for snapshot in app.get_state_history(config):
        print(snapshot.config["configurable"].get("checkpoint_id"), snapshot.values)

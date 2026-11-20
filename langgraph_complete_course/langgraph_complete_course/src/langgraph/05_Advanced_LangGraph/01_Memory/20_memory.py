from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.store.memory import InMemoryStore

class State(TypedDict):
    user_id: str
    preference: str
    reply: str

store = InMemoryStore()

def remember(state: State):
    store.put((state["user_id"], "preferences"), "style", {"value": state["preference"]})
    return {"reply": f"Saved preference: {state['preference']}"}

def recall(state: State):
    item = store.get((state["user_id"], "preferences"), "style")
    value = item.value["value"] if item else "No saved preference"
    return {"reply": f"Remembered preference: {value}"}

builder = StateGraph(State)
builder.add_node("remember", remember)
builder.add_node("recall", recall)
builder.add_edge(START, "remember")
builder.add_edge("remember", "recall")
builder.add_edge("recall", END)
app = builder.compile(store=store)

if __name__ == "__main__":
    print(app.invoke({"user_id": "student-1", "preference": "simple explanations", "reply": ""}))

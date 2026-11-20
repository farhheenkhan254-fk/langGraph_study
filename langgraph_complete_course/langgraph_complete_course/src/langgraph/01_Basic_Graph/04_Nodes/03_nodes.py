from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    text: str
    cleaned: str
    word_count: int

def clean_text(state: State):
    return {"cleaned": " ".join(state["text"].strip().lower().split())}

def count_words(state: State):
    return {"word_count": len(state["cleaned"].split())}

builder = StateGraph(State)
builder.add_node("clean", clean_text)
builder.add_node("count", count_words)
builder.add_edge(START, "clean")
builder.add_edge("clean", "count")
builder.add_edge("count", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"text": "  LangGraph   has Nodes  ", "cleaned": "", "word_count": 0}))

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    topic: str
    outline: str
    summary: str

def create_outline(state: State):
    return {"outline": f"1. Definition of {state['topic']}\\n2. Uses\\n3. Example"}

def summarize(state: State):
    return {"summary": f"Study outline created for {state['topic']} with 3 sections."}

builder = StateGraph(State)
builder.add_node("outline", create_outline)
builder.add_node("summary", summarize)
builder.add_edge(START, "outline")
builder.add_edge("outline", "summary")
builder.add_edge("summary", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"topic": "Knowledge Graph", "outline": "", "summary": ""}))

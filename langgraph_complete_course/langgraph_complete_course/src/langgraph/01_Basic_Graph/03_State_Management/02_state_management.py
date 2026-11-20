from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    numbers: list[int]
    total: int
    note: str

def calculate(state: State):
    total = sum(state["numbers"])
    return {"total": total, "note": f"Added {len(state['numbers'])} numbers"}

builder = StateGraph(State)
builder.add_node("calculate", calculate)
builder.add_edge(START, "calculate")
builder.add_edge("calculate", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"numbers": [10, 20, 30], "total": 0, "note": ""}))

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    task: str
    team: str
    result: str

def supervisor(state: State):
    team = "researcher" if "research" in state["task"].lower() else "writer"
    return {"team": team}

def route(state: State) -> Literal["researcher", "writer"]:
    return state["team"]

def researcher(state: State):
    return {"result": f"Research notes prepared for: {state['task']}"}

def writer(state: State):
    return {"result": f"Draft prepared for: {state['task']}"}

builder = StateGraph(State)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route, {"researcher": "researcher", "writer": "writer"})
builder.add_edge("researcher", END)
builder.add_edge("writer", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"task": "Research LangGraph checkpointing", "team": "", "result": ""}))

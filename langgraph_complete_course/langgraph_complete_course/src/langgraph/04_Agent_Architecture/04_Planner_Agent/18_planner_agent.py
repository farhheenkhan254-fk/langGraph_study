from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    goal: str
    plan: list[str]
    completed: list[str]

def plan_steps(state: State):
    return {"plan": [f"Understand {state['goal']}", "Break the goal into tasks", "Execute and review"]}

def execute(state: State):
    return {"completed": [f"Completed: {step}" for step in state["plan"]]}

builder = StateGraph(State)
builder.add_node("planner", plan_steps)
builder.add_node("executor", execute)
builder.add_edge(START, "planner")
builder.add_edge("planner", "executor")
builder.add_edge("executor", END)
app = builder.compile()

if __name__ == "__main__":
    print(app.invoke({"goal": "learn LangGraph", "plan": [], "completed": []}))

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# ============================================================
# TOPIC 1: BASIC LANGGRAPH
# ============================================================

from typing import TypedDict

# StateGraph: Main class for creating a graph.
# START: Starting point of the graph.
# END: Ending point of the graph.

from langgraph.graph import StateGraph, START, END


# ============================================================
# STEP 1: DEFINE STATE
# ============================================================

# TypedDict defines the structure of our State.
# State is shared data that Nodes can read and update.

class SchoolState(TypedDict):

    user_name: str
    message: str
    


# ============================================================
# STEP 2: CREATE NODE
# ============================================================

# A Node is a Python function that performs a task.
# It receives the current State and returns an update.

def welcome_node(state: SchoolState):

    print("Welcome Node Executed")

    return {
        "message": f"Welcome {state['user_name']}!"
    }


# ============================================================
# STEP 3: CREATE GRAPH
# ============================================================

# StateGraph creates the graph using SchoolState.

graph = StateGraph(SchoolState)


# ============================================================
# STEP 4: ADD NODE
# ============================================================

# add_node() registers a Python function in the graph.

graph.add_node("welcome", welcome_node)


# ============================================================
# STEP 5: ADD EDGES
# ============================================================

# START -> welcome -> END

graph.add_edge(START, "welcome")
graph.add_edge("welcome", END)


# ============================================================
# STEP 6: COMPILE GRAPH
# ============================================================

# compile() prepares the graph for execution.

app = graph.compile()


# ============================================================
# STEP 7: INITIAL STATE
# ============================================================

initial_state = {
    "user_name": "Farheen",
    "message": ""
}


# ============================================================
# STEP 8: EXECUTE GRAPH
# ============================================================

# invoke() starts graph execution and returns final State.

result = app.invoke(initial_state)


# ============================================================
# STEP 9: FINAL OUTPUT
# ============================================================

print("\nFinal Output:")
print(result)

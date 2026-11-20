from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# ============================================================
# TOPIC 4: EDGES IN LANGGRAPH
# ============================================================

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ============================================================
# STEP 1: DEFINE STATE
# ============================================================

class SchoolState(TypedDict):

    student_name: str
    message: str


# ============================================================
# STEP 2: CREATE NODES
# ============================================================

def admission_node(state: SchoolState):

    print("Admission Node Executed")

    return {
        "message": "Admission process started"
    }


def verification_node(state: SchoolState):

    print("Verification Node Executed")

    return {
        "message": state["message"] + " | Documents verified"
    }


def registration_node(state: SchoolState):

    print("Registration Node Executed")

    return {
        "message": state["message"] + " | Student registered"
    }


# ============================================================
# STEP 3: CREATE GRAPH
# ============================================================

graph = StateGraph(SchoolState)


# ============================================================
# STEP 4: ADD NODES
# ============================================================

graph.add_node("admission", admission_node)
graph.add_node("verification", verification_node)
graph.add_node("registration", registration_node)


# ============================================================
# STEP 5: CONNECT USING NORMAL EDGES
# ============================================================

# Normal Edges define a fixed execution path.
#
# START -> admission
# admission -> verification
# verification -> registration
# registration -> END

graph.add_edge(START, "admission")

graph.add_edge("admission", "verification")

graph.add_edge("verification", "registration")

graph.add_edge("registration", END)


# ============================================================
# STEP 6: COMPILE
# ============================================================

app = graph.compile()


# ============================================================
# STEP 7: INITIAL STATE
# ============================================================

initial_state = {
    "student_name": "Rahul",
    "message": ""
}


# ============================================================
# STEP 8: EXECUTE
# ============================================================

result = app.invoke(initial_state)


# ============================================================
# STEP 9: DISPLAY RESULT
# ============================================================

print("\nFinal Result:")
print(result)

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# ============================================================
# TOPIC 3: STATE REDUCERS
# ============================================================

from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END


# ============================================================
# STEP 1: DEFINE STATE
# ============================================================

# Annotated attaches a Reducer to the messages field.
#
# operator.add combines the old list and new list.
#
# Example:
# Old: ["Hello"]
# New: ["Welcome"]
# Result: ["Hello", "Welcome"]

class SchoolState(TypedDict):

    student_name: str

    messages: Annotated[list, operator.add]


# ============================================================
# STEP 2: CREATE WELCOME NODE
# ============================================================

def welcome_node(state: SchoolState):

    print("Welcome Node Executed")

    return {
        "messages": [
            f"Welcome {state['student_name']}"
        ]
    }


# ============================================================
# STEP 3: CREATE ATTENDANCE NODE
# ============================================================

def attendance_node(state: SchoolState):

    print("Attendance Node Executed")

    return {
        "messages": [
            "Attendance is 95%"
        ]
    }


# ============================================================
# STEP 4: CREATE HOMEWORK NODE
# ============================================================

def homework_node(state: SchoolState):

    print("Homework Node Executed")

    return {
        "messages": [
            "Homework is pending"
        ]
    }


# ============================================================
# STEP 5: CREATE GRAPH
# ============================================================

graph = StateGraph(SchoolState)


# ============================================================
# STEP 6: ADD NODES
# ============================================================

graph.add_node("welcome", welcome_node)
graph.add_node("attendance", attendance_node)
graph.add_node("homework", homework_node)


# ============================================================
# STEP 7: ADD EDGES
# ============================================================

graph.add_edge(START, "welcome")
graph.add_edge("welcome", "attendance")
graph.add_edge("attendance", "homework")
graph.add_edge("homework", END)


# ============================================================
# STEP 8: COMPILE
# ============================================================

app = graph.compile()


# ============================================================
# STEP 9: INITIAL STATE
# ============================================================

initial_state = {
    "student_name": "Rahul",
    "messages": []
}


# ============================================================
# STEP 10: EXECUTE
# ============================================================

result = app.invoke(initial_state)


# ============================================================
# STEP 11: DISPLAY RESULT
# ============================================================

print("\nFinal Messages:")

for message in result["messages"]:

    print("-", message)

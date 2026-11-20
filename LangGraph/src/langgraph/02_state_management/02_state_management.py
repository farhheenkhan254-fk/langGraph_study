from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# ============================================================
# TOPIC 2: STATE MANAGEMENT
# ============================================================

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ============================================================
# STEP 1: DEFINE STATE
# ============================================================

# TypedDict defines all fields available in our State.
#
# str = String
# int = Integer
# bool = Boolean

class SchoolState(TypedDict):

    student_name: str
    age: int
    attendance: bool
    message: str


# ============================================================
# STEP 2: CREATE FIRST NODE
# ============================================================

def student_node(state: SchoolState):

    print("Student Node Executed")

    # Read student details from State.
    # Return an update to the message field.

    return {
        "message": f"Student Name: {state['student_name']}"
    }


# ============================================================
# STEP 3: CREATE SECOND NODE
# ============================================================

def attendance_node(state: SchoolState):

    print("Attendance Node Executed")

    # Read the attendance field.
    # Add the attendance result to the message.

    if state["attendance"]:

        attendance_message = "Student is Present"

    else:

        attendance_message = "Student is Absent"

    return {
        "message": state["message"] + " | " + attendance_message
    }


# ============================================================
# STEP 4: CREATE GRAPH
# ============================================================

graph = StateGraph(SchoolState)


# ============================================================
# STEP 5: ADD NODES
# ============================================================

graph.add_node("student", student_node)
graph.add_node("attendance", attendance_node)


# ============================================================
# STEP 6: CONNECT NODES
# ============================================================

graph.add_edge(START, "student")
graph.add_edge("student", "attendance")
graph.add_edge("attendance", END)


# ============================================================
# STEP 7: COMPILE
# ============================================================

app = graph.compile()


# ============================================================
# STEP 8: INITIAL STATE
# ============================================================

initial_state = {

    "student_name": "Rahul",
    "age": 15,
    "attendance": True,
    "message": ""

}


# ============================================================
# STEP 9: EXECUTE
# ============================================================

result = app.invoke(initial_state)


# ============================================================
# STEP 10: DISPLAY RESULT
# ============================================================

print("\nFinal State:")
print(result)

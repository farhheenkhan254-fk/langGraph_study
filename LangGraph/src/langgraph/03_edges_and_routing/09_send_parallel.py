from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# ============================================================
# TOPIC 9: SEND AND PARALLEL EXECUTION
# ============================================================

from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


# ============================================================
# STEP 1: DEFINE MAIN STATE
# ============================================================

class OverallState(TypedDict):

    # Contains all student names.

    students: list[str]

    # Stores attendance results from parallel tasks.
    #
    # operator.add combines results from different tasks.

    results: Annotated[list, operator.add]


# ============================================================
# STEP 2: DEFINE WORKER STATE
# ============================================================

# Each worker receives one student's name.
#
# This is a separate input schema for the worker Node.

class WorkerState(TypedDict):

    student_name: str


# ============================================================
# STEP 3: CREATE WORKER NODE
# ============================================================

def attendance_worker(state: WorkerState):

    # Each execution processes one student.
    #
    # Send can create multiple executions of this Node
    # with different student_name values.

    student = state["student_name"]

    print(f"Processing attendance for {student}")

    # Return the attendance result.
    # The results Reducer combines outputs.

    return {
        "results": [
            f"{student}: Attendance checked"
        ]
    }


# ============================================================
# STEP 4: CREATE ROUTER FUNCTION
# ============================================================

def distribute_students(state: OverallState):

    # Send dynamically creates tasks.
    #
    # Each Send contains:
    # First argument -> Name of the target Node.
    # Second argument -> State/input for that execution.
    #
    # One worker execution is created for each student.

    return [

        Send(
            "attendance_worker",
            {"student_name": student}
        )

        for student in state["students"]

    ]


# ============================================================
# STEP 5: CREATE GRAPH
# ============================================================

graph = StateGraph(OverallState)


# ============================================================
# STEP 6: ADD WORKER NODE
# ============================================================

graph.add_node("attendance_worker", attendance_worker)


# ============================================================
# STEP 7: ADD DYNAMIC ROUTING
# ============================================================

# START sends execution to dynamically created worker tasks.

graph.add_conditional_edges(
    START,
    distribute_students
)


# ============================================================
# STEP 8: CONNECT WORKERS TO END
# ============================================================

graph.add_edge("attendance_worker", END)


# ============================================================
# STEP 9: COMPILE
# ============================================================

app = graph.compile()


# ============================================================
# STEP 10: INITIAL STATE
# ============================================================

initial_state = {

    "students": [
        "Rahul",
        "Aman",
        "Priya"
    ],

    "results": []

}


# ============================================================
# STEP 11: EXECUTE
# ============================================================

result = app.invoke(initial_state)


# ============================================================
# STEP 12: DISPLAY RESULTS
# ============================================================

print("\nFinal Attendance Results:")

for item in result["results"]:

    print("-", item)

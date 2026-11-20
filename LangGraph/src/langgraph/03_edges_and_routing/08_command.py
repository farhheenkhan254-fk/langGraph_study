from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# ============================================================
# TOPIC 8: COMMAND IN LANGGRAPH
# ============================================================

from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command


# ============================================================
# STEP 1: DEFINE STATE
# ============================================================

class SchoolState(TypedDict):

    student_name: str
    attendance: bool
    result: str


# ============================================================
# STEP 2: CREATE ATTENDANCE NODE
# ============================================================

def attendance_node(state: SchoolState):

    print("Attendance Node Executed")

    # Check the student's attendance.
    #
    # Command can update State and choose the next Node.

    if state["attendance"]:

        # update:
        # Updates the result field.
        #
        # goto:
        # Directs execution to the homework Node.

        return Command(
            update={
                "result": "Student is present"
            },
            goto="homework"
        )

    else:

        # If the student is absent,
        # route directly to the absence Node.

        return Command(
            update={
                "result": "Student is absent"
            },
            goto="absence"
        )


# ============================================================
# STEP 3: CREATE HOMEWORK NODE
# ============================================================

def homework_node(state: SchoolState):

    print("Homework Node Executed")

    return {
        "result": state["result"] + " | Homework assigned"
    }


# ============================================================
# STEP 4: CREATE ABSENCE NODE
# ============================================================

def absence_node(state: SchoolState):

    print("Absence Node Executed")

    return {
        "result": state["result"] + " | Absence recorded"
    }


# ============================================================
# STEP 5: CREATE GRAPH
# ============================================================

graph = StateGraph(SchoolState)


# ============================================================
# STEP 6: REGISTER NODES
# ============================================================

graph.add_node("attendance", attendance_node)
graph.add_node("homework", homework_node)
graph.add_node("absence", absence_node)


# ============================================================
# STEP 7: ADD START EDGE
# ============================================================

graph.add_edge(START, "attendance")


# ============================================================
# STEP 8: ADD END EDGES
# ============================================================

graph.add_edge("homework", END)
graph.add_edge("absence", END)


# ============================================================
# STEP 9: COMPILE
# ============================================================

app = graph.compile()


# ============================================================
# STEP 10: INITIAL STATE
# ============================================================

initial_state = {

    "student_name": "Rahul",

    # Change True to False to test the other route.

    "attendance": True,

    "result": ""

}


# ============================================================
# STEP 11: EXECUTE
# ============================================================

result = app.invoke(initial_state)


# ============================================================
# STEP 12: DISPLAY RESULT
# ============================================================

print("\nFinal Result:")
print(result)


# Important properties:
# - update: Updates the State.
# - goto: Specifies the next Node.
# - graph: Can specify a target graph when working with subgraphs.
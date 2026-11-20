from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# ============================================================
# TOPIC 5: CONDITIONAL EDGES
# ============================================================

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


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

def check_attendance(state: SchoolState):

    print("Attendance Check Node Executed")

    # This Node reads the attendance value.
    # It does not decide which Node runs next.
    # The Router function will make that decision.

    return {
        "result": "Attendance checked"
    }


# ============================================================
# STEP 3: CREATE ROUTER FUNCTION
# ============================================================

# A Router is a normal Python function.
#
# It reads the current State and returns a Node name.
#
# The returned Node name must match a registered graph Node.

def attendance_router(state: SchoolState):

    # Check whether the student is present.

    if state["attendance"] == True:

        return "present"

    else:

        return "absent"


# ============================================================
# STEP 4: CREATE PRESENT NODE
# ============================================================

def homework_node(state: SchoolState):

    print("Homework Node Executed")

    return {
        "result": "Student is present. Homework assigned."
    }


# ============================================================
# STEP 5: CREATE ABSENT NODE
# ============================================================

def absence_node(state: SchoolState):

    print("Absence Node Executed")

    return {
        "result": "Student is absent. Attendance marked."
    }


# ============================================================
# STEP 6: CREATE GRAPH
# ============================================================

graph = StateGraph(SchoolState)


# ============================================================
# STEP 7: REGISTER NODES
# ============================================================

graph.add_node("check_attendance", check_attendance)

graph.add_node("homework", homework_node)

graph.add_node("absence", absence_node)


# ============================================================
# STEP 8: ADD NORMAL EDGES
# ============================================================

graph.add_edge(START, "check_attendance")


# ============================================================
# STEP 9: ADD CONDITIONAL EDGE
# ============================================================

# add_conditional_edges() connects a Node to a Router.
#
# First argument:
# The Node after which routing should happen.
#
# Second argument:
# The Router function that selects the next Node.
#
# Third argument:
# Mapping between Router return values and Node names.

graph.add_conditional_edges(

    "check_attendance",

    attendance_router,

    {
        "present": "homework",
        "absent": "absence"
    }

)


# ============================================================
# STEP 10: CONNECT BOTH ROUTES TO END
# ============================================================

graph.add_edge("homework", END)

graph.add_edge("absence", END)


# ============================================================
# STEP 11: COMPILE GRAPH
# ============================================================

app = graph.compile()


# ============================================================
# STEP 12: INITIAL STATE
# ============================================================

initial_state = {

    "student_name": "Rahul",

    # Change this to False to test the absent route.

    "attendance": True,

    "result": ""

}


# ============================================================
# STEP 13: EXECUTE GRAPH
# ============================================================

result = app.invoke(initial_state)


# ============================================================
# STEP 14: DISPLAY FINAL RESULT
# ============================================================

print("\nFinal Result:")
print(result)

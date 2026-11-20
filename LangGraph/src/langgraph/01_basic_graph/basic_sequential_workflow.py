from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# from typing import TypedDict
# from langgraph.graph import StateGraph, START, END


# # STEP 1: Define State
# class SchoolState(TypedDict):
#     user_name: str
#     message: str


# # STEP 2: Create Node 1
# def welcome_node(state: SchoolState):

#     print("Welcome Node Executed")

#     return {
#         "message": f"Hello {state['user_name']}! Welcome to LangGraph."
#     }


# # STEP 3: Create Node 2
# def response_node(state: SchoolState):

#     print("Response Node Executed")

#     return {
#         "message": state["message"] + " Your first graph is working!"
#     }


# # STEP 4: Create StateGraph
# graph = StateGraph(SchoolState)


# # STEP 5: Add Nodes
# graph.add_node("welcome", welcome_node)
# graph.add_node("response", response_node)


# # STEP 6: Connect Nodes with Edges
# graph.add_edge(START, "welcome")
# graph.add_edge("welcome", "response")
# graph.add_edge("response", END)


# # STEP 7: Compile Graph
# app = graph.compile()


# # STEP 8: Execute Graph
# initial_state = {
#     "user_name": "Farheen",
#     "message": ""
# }

# result = app.invoke(initial_state)


# # STEP 9: Print Final Result
# print("\nFinal Output:")
# print(result)
# =========================


#
# ============================================================
# LESSON 1: BASIC LANGGRAPH + STATE MANAGEMENT
# ============================================================

# -------------------- PYTHON IMPORTS -------------------------

# TypedDict:
# Used to define the structure of our State.
#
# Annotated:
# Used to attach additional information to a State field.
# In LangGraph, we can use it to define a Reducer.
#
# operator:
# A built-in Python module.
# operator.add will be used to combine lists.

from typing import TypedDict, Annotated
import operator


# -------------------- LANGGRAPH IMPORTS ----------------------

# StateGraph:
# Main class used to create a LangGraph workflow.
#
# START:
# Special starting point of the graph.
#
# END:
# Special ending point of the graph.

from langgraph.graph import StateGraph, START, END


# ============================================================
# STEP 1: DEFINE STATE
# ============================================================

# WHAT IS STATE?
#
# State is the shared data structure of a graph.
# Every Node can receive the current State.
# Nodes can read its values and return updates.
#
# WHAT IS TYPEDDICT?
#
# TypedDict defines which fields are available
# and their expected data types.
#
# WHAT IS A REDUCER?
#
# A Reducer defines how old and new values
# are combined when a State field is updated.
#
# Without a Reducer:
# The new value replaces the old value.
#
# With operator.add:
# Old and new lists are concatenated.

class SchoolState(TypedDict):

    # str means this field stores a string.
    user_name: str

    # Annotated attaches a Reducer to this field.
    #
    # list:
    # The messages field stores a list.
    #
    # operator.add:
    # Combines the existing list with the new list.
    #
    # Example:
    # Old = ["Hello"]
    # New = ["Welcome"]
    # Result = ["Hello", "Welcome"]

    messages: Annotated[list, operator.add]


# ============================================================
# STEP 2: CREATE FIRST NODE
# ============================================================

# WHAT IS A NODE?
#
# A Node is a Python function that performs a task.
#
# LangGraph passes the current State to this function.
# The function reads State values and returns updates.
#
# state: SchoolState
# Means the function receives data following
# our SchoolState structure.

def welcome_node(state: SchoolState):

    print("Welcome Node Executed")

    # Read the user's name from State.
    #
    # Return a dictionary containing the State update.
    #
    # Since messages has operator.add as its Reducer,
    # this new message will be added to the existing list.

    return {
        "messages": [
            f"Hello {state['user_name']}! Welcome to LangGraph."
        ]
    }


# ============================================================
# STEP 3: CREATE SECOND NODE
# ============================================================

def response_node(state: SchoolState):

    print("Response Node Executed")

    # This Node adds another message.
    #
    # The existing messages are available in State.
    # We return only the new message.
    #
    # operator.add combines it with previous messages.

    return {
        "messages": [
            "Your first LangGraph workflow is working!"
        ]
    }


# ============================================================
# STEP 4: CREATE STATE GRAPH
# ============================================================

# StateGraph is the main graph-building class.
#
# SchoolState is passed as the State schema.
#
# It tells LangGraph what data structure
# the Nodes will receive and update.

graph = StateGraph(SchoolState)


# ============================================================
# STEP 5: ADD NODES TO GRAPH
# ============================================================

# add_node() registers a Python function in the graph.
#
# First argument:
# The unique name of the Node.
#
# Second argument:
# The Python function that will execute.

graph.add_node("welcome", welcome_node)

graph.add_node("response", response_node)


# ============================================================
# STEP 6: CONNECT NODES USING EDGES
# ============================================================

# WHAT IS AN EDGE?
#
# An Edge defines the execution path between Nodes.
#
# START -> welcome
# welcome -> response
# response -> END

graph.add_edge(START, "welcome")

graph.add_edge("welcome", "response")

graph.add_edge("response", END)


# ============================================================
# STEP 7: COMPILE GRAPH
# ============================================================

# compile() prepares the graph for execution.
#
# It creates an executable graph application.
#
# We can use this compiled application with:
# invoke()
# stream()

app = graph.compile()


# ============================================================
# STEP 8: DEFINE INITIAL STATE
# ============================================================

# Initial State is the starting data provided to the graph.
#
# user_name:
# Stores the user's name.
#
# messages:
# Starts with an empty list.
#
# This initial State is passed to the first Node.

initial_state = {

    "user_name": "Farheen",

    "messages": []

}


# ============================================================
# STEP 9: EXECUTE GRAPH
# ============================================================

# invoke() starts graph execution.
#
# Execution order:
#
# START
#   |
# welcome_node
#   |
# response_node
#   |
# END
#
# Each Node receives the latest State.
# Its returned updates are applied to the State.
#
# The final State is stored in result.

result = app.invoke(initial_state)


# ============================================================
# STEP 10: DISPLAY FINAL RESULT
# ============================================================

print("\nFinal Output:")

print(result)


# ============================================================
# STEP 11: DISPLAY MESSAGES
# ============================================================

# Loop through the final messages list.
# The Reducer has combined messages from both Nodes.

print("\nAll Messages:")

for message in result["messages"]:

    print("-", message)


# ============================================================
# END OF LESSON 1
# ============================================================

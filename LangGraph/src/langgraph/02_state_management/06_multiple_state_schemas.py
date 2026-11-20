from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# ============================================================
# TOPIC 6: MULTIPLE STATE SCHEMAS
# ============================================================

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ============================================================
# STEP 1: DEFINE INPUT STATE
# ============================================================

# InputState defines which data the user can provide
# when starting the graph.

class InputState(TypedDict):

    user_name: str


# ============================================================
# STEP 2: DEFINE INTERNAL STATE
# ============================================================

# OverallState defines all data available inside
# the graph during execution.
#
# It includes user input and internal processing fields.

class OverallState(TypedDict):

    user_name: str
    processed_message: str
    internal_status: str


# ============================================================
# STEP 3: DEFINE OUTPUT STATE
# ============================================================

# OutputState defines which data should be returned
# as the final graph output.

class OutputState(TypedDict):

    processed_message: str


# ============================================================
# STEP 4: CREATE NODE
# ============================================================

def process_user(state: OverallState):

    print("Process User Node Executed")

    # Read the user's name from the State.
    # Create a processed message.

    return {
        "processed_message": f"Welcome {state['user_name']}!",
        "internal_status": "Processing completed"
    }


# ============================================================
# STEP 5: CREATE GRAPH
# ============================================================

# StateGraph receives:
# OverallState -> Internal State schema.
# InputState   -> Input schema.
# OutputState  -> Output schema.

graph = StateGraph(
    OverallState,
    input_schema=InputState,
    output_schema=OutputState
)


# ============================================================
# STEP 6: ADD NODE
# ============================================================

graph.add_node("process_user", process_user)


# ============================================================
# STEP 7: CONNECT NODES
# ============================================================

graph.add_edge(START, "process_user")
graph.add_edge("process_user", END)


# ============================================================
# STEP 8: COMPILE
# ============================================================

app = graph.compile()


# ============================================================
# STEP 9: PROVIDE INPUT
# ============================================================

initial_input = {
    "user_name": "Farheen"
}


# ============================================================
# STEP 10: EXECUTE
# ============================================================

result = app.invoke(initial_input)


# ============================================================
# STEP 11: DISPLAY OUTPUT
# ============================================================

print("\nFinal Output:")
print(result)

# OutputState controls the final output.
# internal_status is not included in the output.

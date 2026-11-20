from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# ============================================================
# TOPIC 7: MESSAGES STATE
# ============================================================

from typing import TypedDict

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from typing import Annotated


# ============================================================
# STEP 1: DEFINE STATE
# ============================================================

class ChatState(TypedDict):

    # Annotated connects the messages field
    # with the add_messages reducer.
    #
    # add_messages manages message updates.
    # It appends new messages and handles updates by ID.

    messages: Annotated[list, add_messages]


# ============================================================
# STEP 2: CREATE CHAT NODE
# ============================================================

def chatbot_node(state: ChatState):

    print("Chatbot Node Executed")

    # Read the latest message from the conversation.

    last_message = state["messages"][-1]

    # Read the text of the user's message.

    user_text = last_message.content

    # Create an AI response.
    # This is a simple Python response, not an LLM call.

    response = AIMessage(
        content=f"You said: {user_text}. How can I help you?"
    )

    # Return the AI message.
    # add_messages will add it to the conversation.

    return {
        "messages": [response]
    }


# ============================================================
# STEP 3: CREATE GRAPH
# ============================================================

graph = StateGraph(ChatState)


# ============================================================
# STEP 4: ADD NODE
# ============================================================

graph.add_node("chatbot", chatbot_node)


# ============================================================
# STEP 5: CONNECT GRAPH
# ============================================================

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)


# ============================================================
# STEP 6: COMPILE
# ============================================================

app = graph.compile()


# ============================================================
# STEP 7: INITIAL CONVERSATION
# ============================================================

initial_state = {

    "messages": [

        # SystemMessage contains instructions for an AI.
        SystemMessage(
            content="You are a helpful school assistant."
        ),

        # HumanMessage represents the user's input.
        HumanMessage(
            content="What is LangGraph?"
        )

    ]

}


# ============================================================
# STEP 8: EXECUTE
# ============================================================

result = app.invoke(initial_state)


# ============================================================
# STEP 9: DISPLAY CONVERSATION
# ============================================================

print("\nConversation:")

for message in result["messages"]:

    print(type(message).__name__, ":", message.content)

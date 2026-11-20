
# ============================================================
# TOPIC 10: LLM INTEGRATION WITH LANGGRAPH
# ============================================================

# os:
# Used to access environment variables.

import os

# TypedDict:
# Defines our State structure.

from typing import TypedDict

# load_dotenv:
# Loads environment variables from the .env file.

from dotenv import load_dotenv

# ChatGroq:
# Connects LangChain to Groq's hosted chat models.

from langchain_groq import ChatGroq

# HumanMessage:
# Represents the user's message.
#
# SystemMessage:
# Contains instructions for the AI model.

from langchain_core.messages import HumanMessage, SystemMessage

# LangGraph components.

from langgraph.graph import StateGraph, START, END


# ============================================================
# STEP 1: LOAD ENVIRONMENT VARIABLES
# ============================================================

# Load the GROQ_API_KEY from the .env file.

load_dotenv()

# Read the API key securely from the environment.

api_key = os.getenv("GROQ_API_KEY")

# Stop execution if the API key is missing.

if not api_key:

    raise ValueError(
        "GROQ_API_KEY not found. Check your .env file."
    )


# ============================================================
# STEP 2: INITIALIZE THE LLM
# ============================================================

# ChatGroq creates a chat model connection.
#
# model:
# Selects the Groq model.
# Use a model currently available in your Groq account.
#
# temperature:
# Controls response randomness.
# 0 means more consistent responses.
#
# api_key:
# Authenticates our application with Groq.

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=api_key
)


# ============================================================
# STEP 3: DEFINE STATE
# ============================================================

class ChatState(TypedDict):

    # Stores the user's question.

    user_query: str

    # Stores the AI's final response.

    response: str


# ============================================================
# STEP 4: CREATE LLM NODE
# ============================================================

def chatbot_node(state: ChatState):

    print("Chatbot Node Executed")

    # SystemMessage provides instructions to the LLM.
    #
    # HumanMessage contains the actual user question.

    messages = [

        SystemMessage(
            content=(
                "You are a helpful AI tutor. "
                "Explain technical concepts in simple English."
            )
        ),

        HumanMessage(
            content=state["user_query"]
        )

    ]

    # invoke() sends messages to the actual LLM.
    #
    # The model returns an AIMessage.
    # Its content contains the generated response.

    ai_response = llm.invoke(messages)

    # Return the LLM response to the graph State.

    return {
        "response": ai_response.content
    }


# ============================================================
# STEP 5: CREATE GRAPH
# ============================================================

graph = StateGraph(ChatState)


# ============================================================
# STEP 6: ADD NODE
# ============================================================

graph.add_node("chatbot", chatbot_node)


# ============================================================
# STEP 7: ADD EDGES
# ============================================================

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)


# ============================================================
# STEP 8: COMPILE GRAPH
# ============================================================

app = graph.compile()


# ============================================================
# STEP 9: INITIAL STATE
# ============================================================

initial_state = {

    "user_query": "What is LangGraph and why is it used?",

    "response": ""

}


# ============================================================
# STEP 10: EXECUTE GRAPH
# ============================================================

# This executes the LangGraph workflow.
# The chatbot Node calls the actual Groq model.

result = app.invoke(initial_state)


# ============================================================
# STEP 11: DISPLAY AI RESPONSE
# ============================================================

print("\nUser Question:")
print(result["user_query"])

print("\nAI Response:")
print(result["response"])



# =======================QWEN3:4b=====================================

# ============================================================
# TOPIC 10: LLM INTEGRATION WITH LANGGRAPH USING OLLAMA
# MODEL: QWEN3:4B
# ============================================================

# TypedDict:
# Defines the structure of our LangGraph State.

from typing import TypedDict

# ChatOllama:
# Connects LangChain with a locally running Ollama model.
#
# Unlike ChatGroq:
# - ChatGroq connects to a cloud-hosted model.
# - ChatOllama connects to a model running locally.
#
# No API key is required for local Ollama.

from langchain_ollama import ChatOllama

# HumanMessage:
# Represents the user's question.
#
# SystemMessage:
# Provides instructions to the AI model.

from langchain_core.messages import HumanMessage, SystemMessage

# LangGraph components.

from langgraph.graph import StateGraph, START, END


# ============================================================
# STEP 1: INITIALIZE THE LOCAL LLM
# ============================================================

# ChatOllama creates a connection to the Ollama server.
#
# model:
# Specifies which downloaded Ollama model to use.
# Here we are using Qwen3 with 4 billion parameters.
#
# temperature:
# Controls the randomness of the response.
# 0 means more consistent responses.
#
# base_url:
# Default Ollama server address.
# Ollama normally runs at http://localhost:11434.
#
# num_predict:
# Limits the maximum number of generated tokens.

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0,
    base_url="http://localhost:11434",
    num_predict=512
)


# ============================================================
# STEP 2: DEFINE LANGGRAPH STATE
# ============================================================

class ChatState(TypedDict):

    # Stores the user's question.

    user_query: str

    # Stores the AI-generated response.

    response: str


# ============================================================
# STEP 3: CREATE THE LLM NODE
# ============================================================

def chatbot_node(state: ChatState):

    print("Chatbot Node Executed")

    # SystemMessage:
    # Defines the AI assistant's role and behavior.

    # HumanMessage:
    # Passes the actual question from the user.

    messages = [

        SystemMessage(
            content=(
                "You are a helpful AI tutor. "
                "Explain technical concepts in simple English. "
                "Give clear and beginner-friendly explanations."
            )
        ),

        HumanMessage(
            content=state["user_query"]
        )

    ]

    # Invoke the local Qwen3 model.
    #
    # LangChain sends the messages to Ollama.
    # Ollama generates the response.
    # The response is returned as an AIMessage.

    ai_response = llm.invoke(messages)

    # Extract the generated text from AIMessage.
    #
    # Return the response as a State update.

    return {
        "response": ai_response.content
    }


# ============================================================
# STEP 4: CREATE THE GRAPH
# ============================================================

# StateGraph:
# Creates a graph using our ChatState schema.

graph = StateGraph(ChatState)


# ============================================================
# STEP 5: ADD THE NODE
# ============================================================

# chatbot:
# The name of our graph node.
#
# chatbot_node:
# The Python function that executes when this node runs.

graph.add_node("chatbot", chatbot_node)


# ============================================================
# STEP 6: CONNECT THE NODES USING EDGES
# ============================================================

# START -> chatbot:
# Graph execution begins at the chatbot node.

graph.add_edge(START, "chatbot")

# chatbot -> END:
# Execution finishes after the chatbot node completes.

graph.add_edge("chatbot", END)


# ============================================================
# STEP 7: COMPILE THE GRAPH
# ============================================================

# compile():
# Validates and prepares the graph for execution.
#
# app:
# The compiled LangGraph application.

app = graph.compile()


# ============================================================
# STEP 8: DEFINE INITIAL STATE
# ============================================================

initial_state = {

    "user_query": "What is LangGraph and why is it used?",

    "response": ""

}


# ============================================================
# STEP 9: EXECUTE THE GRAPH
# ============================================================

# invoke():
# Starts graph execution with the initial state.
#
# Flow:
# START -> chatbot_node -> Qwen3 LLM -> END
#
# The final State contains the AI-generated response.

result = app.invoke(initial_state)


# ============================================================
# STEP 10: DISPLAY THE RESULT
# ============================================================

print("\nUser Question:")
print(result["user_query"])

print("\nAI Response:")
print(result["response"])

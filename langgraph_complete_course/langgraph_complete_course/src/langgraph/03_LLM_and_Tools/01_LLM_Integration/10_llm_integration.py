import os
from typing import TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

class State(TypedDict):
    question: str
    answer: str

llm = ChatOllama(model=MODEL, base_url=BASE_URL, temperature=0)

def ask_llm(state: State):
    response = llm.invoke(state["question"])
    return {"answer": response.content}

builder = StateGraph(State)
builder.add_node("ask_llm", ask_llm)
builder.add_edge(START, "ask_llm")
builder.add_edge("ask_llm", END)
app = builder.compile()

if __name__ == "__main__":
    result = app.invoke({"question": "Explain LangGraph in simple words.", "answer": ""})
    print(result["answer"])

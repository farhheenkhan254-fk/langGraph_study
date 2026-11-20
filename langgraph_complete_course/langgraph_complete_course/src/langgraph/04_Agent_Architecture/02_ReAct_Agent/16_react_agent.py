import os
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

@tool
def word_count(text: str) -> int:
    """Count the words in the provided text."""
    return len(text.split())

if __name__ == "__main__":
    model = ChatOllama(model=os.getenv("OLLAMA_MODEL", "qwen3:4b"), temperature=0)
    agent = create_react_agent(model, tools=[word_count])
    result = agent.invoke({"messages": [{"role": "user", "content": "Use the word_count tool on: LangGraph makes workflows stateful and controllable."}]})
    for message in result["messages"]:
        if getattr(message, "content", None):
            print(message.type, ":", message.content)

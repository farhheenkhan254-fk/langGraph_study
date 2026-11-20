from langchain_core.tools import tool
from langchain_ollama import ChatOllama
import os

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two whole numbers and return the sum."""
    return a + b

def main():
    model = ChatOllama(model=os.getenv("OLLAMA_MODEL", "qwen3:4b"), temperature=0)
    model_with_tools = model.bind_tools([add_numbers])
    response = model_with_tools.invoke("Use the add_numbers tool to add 17 and 25.")
    print("Model response:", response.content)
    print("Tool calls:", response.tool_calls)
    if response.tool_calls:
        for call in response.tool_calls:
            if call["name"] == "add_numbers":
                print("Tool result:", add_numbers.invoke(call["args"]))

if __name__ == "__main__":
    main()

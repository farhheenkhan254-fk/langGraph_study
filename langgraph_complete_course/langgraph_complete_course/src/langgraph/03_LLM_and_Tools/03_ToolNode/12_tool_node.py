from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

tool_node = ToolNode([multiply])

if __name__ == "__main__":
    message = HumanMessage(
        content="",
        tool_calls=[{"name": "multiply", "args": {"a": 6, "b": 7}, "id": "call_1", "type": "tool_call"}],
    )
    result = tool_node.invoke({"messages": [message]})
    print(result)

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage

@tool
def get_weather(city: str) -> str:
    """Return sample weather for a city. This is mock data, not live weather."""
    return f"Sample weather for {city}: 28°C and partly cloudy."

tools = [get_weather]
executor = ToolNode(tools)

if __name__ == "__main__":
    ai_message = AIMessage(
        content="",
        tool_calls=[{"name": "get_weather", "args": {"city": "Bhopal"}, "id": "weather_1", "type": "tool_call"}],
    )
    print(executor.invoke({"messages": [ai_message]}))

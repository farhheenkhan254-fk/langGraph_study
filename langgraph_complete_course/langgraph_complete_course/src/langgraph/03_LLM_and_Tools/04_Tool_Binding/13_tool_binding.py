import os
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

@tool
def get_course_info(course: str) -> str:
    """Return a short description of a programming course."""
    courses = {"langgraph": "Build stateful graph workflows and agents."}
    return courses.get(course.lower(), "Course information not found.")

if __name__ == "__main__":
    llm = ChatOllama(model=os.getenv("OLLAMA_MODEL", "qwen3:4b"), temperature=0)
    bound_llm = llm.bind_tools([get_course_info])
    response = bound_llm.invoke("Find information about the LangGraph course using the tool.")
    print("Text:", response.content)
    print("Requested tool calls:", response.tool_calls)

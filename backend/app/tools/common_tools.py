from langchain_core.messages import ToolMessage

def handle_tool_error(state) -> dict:
    """
    Function to handle errors during tool execution.
    """
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\nLet me try a different approach.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableLambda

def create_tool_node_with_fallback(tools: list) -> ToolNode:
    """
    Create a tool node with error handling.
    """
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)],
        exception_key="error"
    )
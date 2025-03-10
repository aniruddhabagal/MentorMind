from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .assistant import TutorAssistant
from .nodes import *
from ..models.student_model import LearningState
from ..tools.math_tools import solve_math_problem
from ..tools.science_tools import explain_science_concept
from ..tools.language_tools import analyze_text
from ..tools.assessment_tools import (
    generate_practice_questions, 
    assess_student_answer,
    update_student_model,
    generate_session_summary
)
from ..tools.common_tools import create_tool_node_with_fallback
from ..prompts.tutor_prompts import create_tutor_prompt
from ..models.llm_setup import create_gemini_llm

def custom_tools_condition(state):
    """
    Custom condition to check if the latest message has tool calls.
    Modified to work with different message formats.
    """
    messages = state.get("messages", [])
    if not messages:
        return END
    
    last_message = messages[-1]
    
    # Check if it's an AIMessage with tool_calls attribute
    if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Check if it's a tuple with assistant message containing tool_calls
    if isinstance(last_message, tuple) and last_message[0] == "assistant":
        content = last_message[1]
        if isinstance(content, dict) and content.get("tool_calls"):
            return "tools"
    
    # No tool calls found
    return END

def build_tutor_graph(llm=None):
    """
    Build and return the complete tutor graph.
    
    Args:
        llm: Optional pre-configured LLM. If None, a new one will be created.
        
    Returns:
        Compiled StateGraph ready for use
    """
    # Create LLM if not provided
    if llm is None:
        llm = create_gemini_llm()
    
    # Define all tools
    tutor_tools = [
        solve_math_problem,
        explain_science_concept,
        analyze_text,
        generate_practice_questions,
        assess_student_answer,
        update_student_model,
        generate_session_summary
    ]
    
    # Create the tutor prompt and bind tools
    tutor_prompt = create_tutor_prompt()
    tutor_runnable = tutor_prompt | llm.bind_tools(tutor_tools)
    
    # Initialize the graph
    builder = StateGraph(LearningState)
    
    # Add the core nodes
    builder.add_node("tutor", TutorAssistant(tutor_runnable))
    builder.add_node("tools", create_tool_node_with_fallback(tutor_tools))
    
    # Add activity nodes
    builder.add_node("concept_introduction", create_introduction_node())
    builder.add_node("practice_session", create_practice_node())
    builder.add_node("assessment", create_assessment_node())
    builder.add_node("adaptive_learning", create_adaptive_node())
    builder.add_node("review", create_review_node())
    builder.add_node("session_summary", create_summary_node(generate_session_summary))
    
    # Define the START state
    builder.set_entry_point("tutor")
    
    # Define standard tool flow - use custom conditional edge
    builder.add_conditional_edges(
        "tutor",
        custom_tools_condition,
        {
            "tools": "tools",
            END: "concept_introduction"  # Default to introduction if no tools
        }
    )
    builder.add_edge("tools", "tutor")
    
    # Add conditional edges based on learning phase
    builder.add_conditional_edges(
        "tutor", 
        lambda state: state.get("learning_phase", "introduction"),
        {
            "introduction": "concept_introduction",
            "practice": "practice_session",
            "assessment": "assessment",
            "review": "review"
        }
    )
    
    # Connect learning activities back to the tutor
    builder.add_edge("concept_introduction", "tutor")
    builder.add_edge("practice_session", "tutor")
    builder.add_edge("assessment", "adaptive_learning")
    builder.add_edge("adaptive_learning", "tutor")
    builder.add_edge("review", "session_summary")
    builder.add_edge("session_summary", "tutor")
    
    # Create memory saver to maintain state
    memory = MemorySaver()
    
    # Compile and return the graph
    return builder.compile(checkpointer=memory)
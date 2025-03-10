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
import logging

logger = logging.getLogger(__name__)

def tutor_routing_condition(state):
    """Combined routing logic for tools, termination, and learning phases."""
    logger.debug(f"Evaluating state: {state}")
    messages = state.get("messages", [])
    
    if not messages:
        return END
    
    last_message = messages[-1]
    
    # Check for tool calls
    if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    if isinstance(last_message, tuple) and last_message[0] == "assistant":
        content = last_message[1]
        if isinstance(content, dict) and content.get("tool_calls"):
            return "tools"
    
    # Stop if tutor has responded
    if state.get("tutor_responded", False):
        return END
    
    # Route based on learning phase if no tools or response yet
    return state.get("learning_phase", "introduction")

def build_tutor_graph(llm=None):
    if llm is None:
        llm = create_gemini_llm()
    
    tutor_tools = [
        solve_math_problem,
        explain_science_concept,
        analyze_text,
        generate_practice_questions,
        assess_student_answer,
        update_student_model,
        generate_session_summary
    ]
    
    tutor_prompt = create_tutor_prompt()
    tutor_runnable = tutor_prompt | llm.bind_tools(tutor_tools)
    
    builder = StateGraph(LearningState)
    
    builder.add_node("tutor", TutorAssistant(tutor_runnable))
    builder.add_node("tools", create_tool_node_with_fallback(tutor_tools))
    builder.add_node("concept_introduction", create_introduction_node())
    builder.add_node("practice_session", create_practice_node())
    builder.add_node("assessment", create_assessment_node())
    builder.add_node("adaptive_learning", create_adaptive_node())
    builder.add_node("review", create_review_node())
    builder.add_node("session_summary", create_summary_node(generate_session_summary))
    
    builder.set_entry_point("tutor")
    
    # Single conditional edge handling all cases
    builder.add_conditional_edges(
        "tutor",
        tutor_routing_condition,
        {
            "tools": "tools",
            END: "__end__",  # Terminate when tutor_responded is True
            "introduction": "concept_introduction",
            "practice": "practice_session",
            "assessment": "assessment",
            "review": "review"
        }
    )
    
    # Define edges back to tutor or other nodes
    builder.add_edge("tools", "tutor")
    builder.add_edge("concept_introduction", "tutor")
    builder.add_edge("practice_session", "tutor")
    builder.add_edge("assessment", "adaptive_learning")
    builder.add_edge("adaptive_learning", "tutor")
    builder.add_edge("review", "session_summary")
    builder.add_edge("session_summary", "tutor")
    
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)
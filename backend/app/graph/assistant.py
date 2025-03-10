from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage
from ..models.student_model import LearningState
import logging

logger = logging.getLogger(__name__)

class TutorAssistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: LearningState):
        logger.debug(f"Input state: {state}")
        try:
            student_profile = state.get("student_profile", {})
            messages = state.get("messages", [])
            input_message = next((msg[1] for msg in messages[::-1] if msg[0] == "user"), "")
            
            # If no phase-specific action is needed, just pass through
            if not input_message or state.get("tutor_responded", False):
                return state
            
            prompt_state = {
                **state,
                "student_grade_level": student_profile.get("grade", 8),
                "learning_style": student_profile.get("learning_style", "visual"),
                "strengths": student_profile.get("strengths", []),
                "areas_for_improvement": state.get("areas_for_improvement", []),
                "input": input_message
            }
            
            result = self.runnable.invoke(prompt_state)
            logger.debug(f"Raw LLM result: {result}")
            
            if isinstance(result, AIMessage):
                messages = state["messages"] + [result]
            elif isinstance(result, list):
                messages = state["messages"] + result
            elif isinstance(result, dict) and "messages" in result:
                return result
            else:
                content = result.content if hasattr(result, "content") else str(result)
                message = ("assistant", content)
                messages = state["messages"] + [message]
            
            updated_state = {"messages": messages, "tutor_responded": True}
            return {**state, **updated_state}
            
        except Exception as e:
            error_message = f"Error processing request: {str(e)}"
            message = ("assistant", error_message)
            return {**state, "messages": state["messages"] + [message], "tutor_responded": True}
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage
from ..models.student_model import LearningState

class TutorAssistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: LearningState):
        try:
            # Extract student profile fields to pass directly to the prompt
            student_profile = state.get("student_profile", {})
            
            # Create a new state with flattened student profile attributes
            prompt_state = {
                **state,
                "student_grade_level": student_profile.get("grade_level", 8),
                "learning_style": student_profile.get("learning_style", "visual"),
                "strengths": student_profile.get("strengths", []),
                "areas_for_improvement": student_profile.get("areas_for_improvement", [])
            }
            
            # Process the current state through the runnable
            result = self.runnable.invoke(prompt_state)
            
            # Check if result is a message or a list of messages
            if isinstance(result, AIMessage):
                return {"messages": state["messages"] + [result]}
            elif isinstance(result, list):
                return {"messages": state["messages"] + result}
            elif isinstance(result, dict) and "messages" in result:
                return result
            else:
                # Create a formatted message from the result content
                if hasattr(result, "content"):
                    content = result.content
                else:
                    content = str(result)
                    
                message = ("assistant", content)
                return {"messages": state["messages"] + [message]}
                
        except Exception as e:
            # Handle exceptions gracefully
            error_message = f"Error processing request: {str(e)}"
            message = ("assistant", error_message)
            return {"messages": state["messages"] + [message]}
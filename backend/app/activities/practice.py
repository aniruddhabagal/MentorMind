from ..models.student_model import LearningState

def run_practice_session(state: LearningState) -> LearningState:
    """Run a practice session with appropriate questions."""
    # Logic to generate practice questions and handle responses
    
    # For now, just update the state to indicate we've moved to the practice phase
    return {
        **state,
        "learning_phase": "practice", 
        "messages": state["messages"]  # In real implementation, would add practice session messages
    }
from ..models.student_model import LearningState

def review_session(state: LearningState) -> LearningState:
    """Review concepts from the session, especially those the student struggled with."""
    # Logic to create personalized review material
    
    # For now, just update the state to indicate we've moved to the review phase
    return {
        **state,
        "learning_phase": "review",
        "messages": state["messages"]  # In real implementation, would add review messages
    }
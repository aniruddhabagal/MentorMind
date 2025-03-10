from ..models.student_model import LearningState

def run_practice_session(state: LearningState) -> LearningState:
    """Run a practice session with appropriate questions."""
    question = "What are the solutions to x² + 5x + 6 = 0?"
    correct_answer = "x = -2, x = -3"  # Store for later assessment
    prompt = f"Now let’s practice! {question}"
    return {
        **state,
        "learning_phase": "assessment",  # Move to assessment after asking
        "current_question": question,    # Store the question
        "correct_answer": correct_answer, # Store the correct answer
        "messages": state["messages"] + [("assistant", prompt)]
    }
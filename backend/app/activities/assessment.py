from ..models.student_model import LearningState
from ..tools.assessment_tools import assess_student_answer

def assess_understanding(state: LearningState) -> LearningState:
    """Assess the student's understanding of concepts."""
    messages = state.get("messages", [])
    last_message = messages[-1] if messages else None
    
    if last_message and last_message[0] == "user":  # Student submitted an answer
        student_answer = last_message[1]
        question = state.get("current_question", "")
        correct_answer = state.get("correct_answer", "")
        
        if question and correct_answer:
            assessment = assess_student_answer.invoke({
                "question": question,
                "correct_answer": correct_answer,
                "student_answer": student_answer
            })
            feedback = (
                f"Your answer: '{student_answer}'\n"
                f"Feedback: {assessment['feedback']}\n"
                f"Score: {assessment['score']}"
            )
            return {
                **state,
                "learning_phase": "review",  # Move to review after assessment
                "questions_answered": state["questions_answered"] + 1,
                "correct_answers": state["correct_answers"] + (1 if assessment["is_correct"] else 0),
                "messages": state["messages"] + [("assistant", feedback)]
            }
    
    # If no answer yet, wait for student response
    return state

def adaptive_learning_node(state: LearningState) -> LearningState:
    """Node to adjust difficulty and approach based on student performance."""
    # Get current performance metrics
    correct_rate = state["correct_answers"] / max(state["questions_answered"], 1)
    
    # Adjust difficulty
    if correct_rate > 0.8:
        # Student is doing well, increase difficulty
        new_state = {**state, "difficulty_level": min(5, state.get("difficulty_level", 3) + 1)}
    elif correct_rate < 0.5:
        # Student is struggling, decrease difficulty
        new_state = {**state, "difficulty_level": max(1, state.get("difficulty_level", 3) - 1)}
    else:
        # Keep current difficulty
        new_state = state
        
    # Update learning phase if needed
    if state.get("learning_phase") == "assessment" and state["questions_answered"] >= 5:
        new_state["learning_phase"] = "review"
    
    return new_state
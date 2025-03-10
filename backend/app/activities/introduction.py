from ..models.student_model import LearningState
from ..tools.math_tools import solve_math_problem

def introduce_concept(state: LearningState) -> LearningState:
    """Introduce a new concept based on current subject and topic."""
    messages = state.get("messages", [])
    last_user_message = next((msg[1] for msg in messages[::-1] if msg[0] == "user"), "")
    student_profile = state.get("student_profile", {})
    grade_level = student_profile.get("grade", 8)
    
    if "solve" in last_user_message.lower() and "x²" in last_user_message:
        # Extract the equation from the message (assuming format like "Solve x²+5x+6 = 0")
        equation = last_user_message.replace("Solve", "").strip()
        explanation = solve_math_problem.invoke({
            "problem": equation,
            "student_grade_level": grade_level
        })
    else:
        explanation = "Let’s start with an introduction to quadratic equations."
    
    return {
        **state,
        "messages": state["messages"] + [("assistant", explanation)],
        "learning_phase": "practice"  # Move to practice phase
    }
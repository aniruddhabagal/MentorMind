from typing import List, Dict, Any, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages

class StudentProfile(TypedDict):
    """Student profile information."""
    name: str
    grade_level: int
    subjects: List[str]
    strengths: List[str]
    areas_for_improvement: List[str]
    learning_style: str
    
class LearningState(TypedDict):
    """Current state of the learning session."""
    messages: Annotated[list[AnyMessage], add_messages]
    current_subject: str
    current_topic: str
    session_goals: List[str]
    student_profile: StudentProfile
    questions_answered: int
    correct_answers: int
    concepts_mastered: List[str]
    concepts_struggling: List[str]
    learning_phase: str
    difficulty_level: int
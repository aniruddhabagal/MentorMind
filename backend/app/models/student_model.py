from typing import Dict, List, Any, TypedDict, Optional
from pydantic import BaseModel

class StudentProfile(BaseModel):
    """Student profile containing learning preferences and history."""
    name: str
    grade_level: int
    learning_style: str  # visual, auditory, kinesthetic, etc.
    strengths: List[str] = []
    areas_for_improvement: List[str] = []
    subjects_of_interest: List[str] = []
    past_sessions: List[Dict[str, Any]] = []
    
    class Config:
        json_schema_extra  = {
            "example": {
                "name": "Alex Johnson",
                "grade_level": 8,
                "learning_style": "visual",
                "strengths": ["problem solving", "critical thinking"],
                "areas_for_improvement": ["memorization", "organization"],
                "subjects_of_interest": ["science", "math"],
                "past_sessions": []
            }
        }

# Define LearningState as a TypedDict for use with LangGraph
class LearningState(TypedDict, total=False):
    messages: List  # List of message tuples or LangChain message objects
    current_subject: str
    current_topic: str
    session_goals: List[str]
    student_profile: Dict[str, Any]
    questions_answered: int
    correct_answers: int
    concepts_mastered: List[str]
    concepts_struggling: List[str]
    learning_phase: str  # introduction, practice, assessment, review
    difficulty_level: int  # 1-5 scale
    error: Optional[Exception]  # For error handling in the graph
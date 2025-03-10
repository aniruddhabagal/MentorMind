from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from uuid import uuid4
from pydantic import BaseModel

from ..models.student_model import StudentProfile, LearningState
from ..graph.builder import build_tutor_graph
from ..models.llm_setup import create_gemini_llm

router = APIRouter()

# Pydantic models for API requests and responses
class Message(BaseModel):
    role: str
    content: str

class MessageRequest(BaseModel):
    message: str
    session_id: str = None

class TutorResponse(BaseModel):
    response: str
    session_id: str
    learning_state: Dict[str, Any]

class SessionRequest(BaseModel):
    student_profile: Dict[str, Any]
    subject: str
    topic: str
    session_goals: List[str] = []

# Store active sessions
active_sessions = {}

@router.post("/sessions", response_model=Dict[str, Any])
async def create_session(request: SessionRequest):
    """Create a new tutoring session."""
    # Generate session ID
    session_id = str(uuid4())
    
    # Initialize learning state
    initial_state = {
        "messages": [],
        "current_subject": request.subject,
        "current_topic": request.topic,
        "session_goals": request.session_goals,
        "student_profile": request.student_profile,
        "questions_answered": 0,
        "correct_answers": 0,
        "concepts_mastered": [],
        "concepts_struggling": [],
        "learning_phase": "introduction",
        "difficulty_level": 3
    }
    
    # Create tutor graph with Gemini LLM
    llm = create_gemini_llm()
    tutor_graph = build_tutor_graph(llm)
    
    # Store session
    active_sessions[session_id] = {
        "graph": tutor_graph,
        "state": initial_state
    }
    
    return {
        "session_id": session_id,
        "message": "Session created successfully",
        "initial_state": initial_state
    }

@router.post("/chat", response_model=TutorResponse)
async def chat(request: MessageRequest):
    """Process a message in a tutoring session."""
    session_id = request.session_id
    
    # Check if session exists
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get session data
    session = active_sessions[session_id]
    current_state = session["state"]
    tutor_graph = session["graph"]
    
    # Update the state with the new user message
    message_state = {
        **current_state,
        "messages": current_state["messages"] + [("user", request.message)]
    }
    
    # Process the message through the graph
    config = {
        "configurable": {
            "thread_id": session_id,
        }
    }
    
    # Run the graph
    result = tutor_graph.invoke(message_state, config)
    
    # Extract response from result
    response_content = ""
    if "messages" in result:
        for message in result["messages"]:
            if hasattr(message, "content") and message.content:
                response_content = message.content
                break
    
    # Update session state
    active_sessions[session_id]["state"] = result
    
    return {
        "response": response_content,
        "session_id": session_id,
        "learning_state": {k: v for k, v in result.items() if k != "messages"}
    }

@router.get("/sessions/{session_id}", response_model=Dict[str, Any])
async def get_session(session_id: str):
    """Get information about a specific session."""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = active_sessions[session_id]
    state = session["state"]
    
    return {
        "session_id": session_id,
        "subject": state["current_subject"],
        "topic": state["current_topic"],
        "learning_phase": state["learning_phase"],
        "progress": {
            "questions_answered": state["questions_answered"],
            "correct_answers": state["correct_answers"],
            "concepts_mastered": state["concepts_mastered"],
            "concepts_struggling": state["concepts_struggling"]
        }
    }

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """End a tutoring session."""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del active_sessions[session_id]
    
    return {"message": "Session deleted successfully"}
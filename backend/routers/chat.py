from fastapi import APIRouter, Depends, HTTPException
from backend.llm_integration import FitnessAssistant
from backend.database import get_db
from sqlalchemy.orm import Session
from backend.schemas import ChatRequest
from backend.models import User, Progress  # Import models

router = APIRouter()
assistant = FitnessAssistant()

@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    # Get user from DB
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get latest progress
    progress = db.query(Progress).filter(
        Progress.user_id == request.user_id
    ).order_by(Progress.date.desc()).first()
    
    # Build context
    user_context = {
        "goals": user.goals,
        "preferences": user.preferences,
        "last_progress": f"{progress.weight}kg, {progress.body_fat}% BF" if progress else "No data"
    }
    
    # Generate response
    response = assistant.generate_response(
        user_input=request.message,
        user_context=user_context
    )
    
    return {"response": response}
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.auth import get_current_user
from app.services.chat_service import ChatService
from app.models import User as DBUser, ChatHistory

router = APIRouter(prefix="/api/chat", tags=["Chat & Code Generation"])

@router.post("/generate")
async def generate_chat(
    prompt: str = Form(...),
    model: str = Form("Groq Llama 3"),
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401, detail="Please login to use this service.")
    
    # Calculate credit cost based on message length
    # Short (< 12) = 1 credit, Medium (> 12) = 2 credits, Long (> 30) = 3 credits
    if len(prompt) > 30:
        CREDIT_COST = 3
    elif len(prompt) > 12:
        CREDIT_COST = 2
    else:
        CREDIT_COST = 1
    
    if user.credits < CREDIT_COST:
        raise HTTPException(status_code=402, detail=f"Insufficient credits. This chat requires {CREDIT_COST} credits.")

    service = ChatService()
    response = await service.generate_response(prompt, model=model)
    
    if "Error:" in response:
        raise HTTPException(status_code=500, detail=response)
    
    # Save chat history
    chat_entry = ChatHistory(
        user_id=user.id,
        message=prompt,
        response=response,
        model_name=model
    )
    db.add(chat_entry)

    # Deduct credits
    user.credits -= CREDIT_COST
    db.commit()
    db.refresh(user)
    
    return {
        "success": True, 
        "response": response, 
        "new_credits": user.credits,
        "chat_id": chat_entry.id
    }

@router.get("/history")
async def get_chat_history(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401, detail="Please login.")
    
    history = db.query(ChatHistory).filter(ChatHistory.user_id == user.id).order_by(ChatHistory.created_at.desc()).all()
    return [{
        "id": c.id,
        "message": c.message,
        "response": c.response,
        "model_name": c.model_name,
        "feedback": c.feedback,
        "created_at": c.created_at.isoformat()
    } for c in history]

@router.post("/feedback")
async def save_feedback(
    chat_id: int = Form(...),
    feedback: str = Form(...), # "Good", "Bad", or "None"
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401, detail="Please login.")
    
    chat_entry = db.query(ChatHistory).filter(ChatHistory.id == chat_id, ChatHistory.user_id == user.id).first()
    if not chat_entry:
        raise HTTPException(status_code=404, detail="Chat not found.")
    
    chat_entry.feedback = feedback if feedback != "None" else None
    db.commit()
    return {"success": True}

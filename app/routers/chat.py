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
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401, detail="Please login to use this service.")
    
    CREDIT_COST = 10
    if user.credits < CREDIT_COST:
        raise HTTPException(status_code=402, detail=f"Insufficient credits. This service costs {CREDIT_COST} credits.")

    service = ChatService()
    response = await service.generate_response(prompt)
    
    if "Error:" in response:
        raise HTTPException(status_code=500, detail=response)
    
    # Save chat history
    chat_entry = ChatHistory(
        user_id=user.id,
        message=prompt,
        response=response,
        model_name="Groq Llama 3"
    )
    db.add(chat_entry)

    # Deduct credits
    user.credits -= CREDIT_COST
    db.commit()
    db.refresh(user)
    
    return {
        "success": True, 
        "response": response, 
        "new_credits": user.credits
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
        "created_at": c.created_at.isoformat()
    } for c in history]

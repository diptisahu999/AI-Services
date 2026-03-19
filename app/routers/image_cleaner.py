from fastapi import APIRouter, UploadFile, File, Form, Request, Depends, HTTPException
from fastapi.responses import Response
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User as DBUser
from app.services.image_cleaner_service import clean_image

router = APIRouter(prefix='/api/image-cleaner', tags=['image-cleaner'])

@router.post('/clean')
async def clean_image_endpoint(
    request: Request,
    file: UploadFile = File(...),
    mode: Optional[str] = Form(None),
    strength: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    # --- Authentication & Credit Check ---
    email = request.cookies.get("session_user")
    if not email:
        raise HTTPException(status_code=401, detail="Please login to use this service.")
    
    user = db.query(DBUser).filter(DBUser.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    
    CREDIT_COST = 8
    if user.credits < CREDIT_COST:
        raise HTTPException(status_code=402, detail=f"Insufficient credits. This service costs {CREDIT_COST} credits.")
    # ------------------------------------

    # Process processing
    content, media_type = await clean_image(file)

    # Deduct credits upon successful processing
    user.credits -= CREDIT_COST
    db.commit()

    return Response(content=content, media_type=media_type)

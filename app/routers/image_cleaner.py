from fastapi import APIRouter, UploadFile, File, Form, Request, Depends, HTTPException
from fastapi.responses import Response
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User as DBUser
from app.services.image_cleaner_service import clean_image

from app.routers.auth import get_current_user

router = APIRouter(prefix='/api/image-cleaner', tags=['image-cleaner'])

@router.post('/clean')
async def clean_image_endpoint(
    file: UploadFile = File(...),
    mode: Optional[str] = Form(None),
    strength: Optional[int] = Form(None),
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401, detail="Please login to use this service.")
    
    CREDIT_COST = 10 # Standardizing to 10 as per previous tasks
    if user.credits < CREDIT_COST:
        raise HTTPException(status_code=402, detail=f"Insufficient credits. This service costs {CREDIT_COST} credits.")

    # Process processing
    content, media_type = await clean_image(file)

    # Deduct credits upon successful processing
    user.credits -= CREDIT_COST
    db.commit()

    return Response(content=content, media_type=media_type, headers={"X-Credits-Left": str(user.credits)})

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.video_translate import fetch_transcript_logic, translate_transcript
from app.routers.auth import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/api/video-translate', tags=['video-translate'])

@router.post('/extract')
async def extract_transcript(
    video_url: str = Form(...), 
    user = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401, detail="Please login to use this service.")
    
    CREDIT_COST = 5
    if user.credits < CREDIT_COST:
        raise HTTPException(status_code=402, detail=f"Insufficient credits. This service costs {CREDIT_COST} credits.")

    # Call the logic
    success, result = fetch_transcript_logic(video_url)
    
    if success:
        # Deduct credits
        user.credits -= CREDIT_COST
        db.commit()
        db.refresh(user)
        
        return {"success": True, "transcript": result, "new_credits": user.credits}
    else:
        return JSONResponse(status_code=500, content={"success": False, "error": result})

@router.post('/translate')
async def translate_video_transcript(
    transcript_text: str = Form(...), 
    target_lang: str = Form("Hindi"),
    user = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401, detail="Please login to use this service.")
    
    CREDIT_COST = 25
    if user.credits < CREDIT_COST:
        raise HTTPException(status_code=402, detail=f"Insufficient credits. This service costs {CREDIT_COST} credits.")

    # Call the translation logic
    success, result = translate_transcript(transcript_text, target_lang)
    
    if success:
        # Deduct credits
        user.credits -= CREDIT_COST
        db.commit()
        db.refresh(user)
        
        return {"success": True, "translated_text": result, "new_credits": user.credits}
    else:
        return JSONResponse(status_code=500, content={"success": False, "error": result})

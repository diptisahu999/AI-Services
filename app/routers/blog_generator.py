from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.blog_generator_service import generate_blog_from_video
from app.routers.auth import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/api/blog', tags=['blog-generator'])

@router.post('/generate')
async def generate_blog_api(
    video_url: str = Form(...), 
    user = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401, detail="Please login to use this service.")
    
    CREDIT_COST = 50
    if user.credits < CREDIT_COST:
        raise HTTPException(status_code=402, detail=f"Insufficient credits. This service costs {CREDIT_COST} credits.")

    # Call the service
    success, result = await generate_blog_from_video(video_url)
    
    if success:
        # Deduct credit after successful generation
        user.credits -= CREDIT_COST
        db.commit()
        db.refresh(user)
        
        return {"success": True, "html": result, "new_credits": user.credits}
    else:
        return JSONResponse(status_code=500, content={"success": False, "error": result})

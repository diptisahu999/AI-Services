from fastapi import APIRouter, HTTPException, Form, Request, Depends
from fastapi.responses import Response
from typing import Optional
from sqlalchemy.orm import Session
from app.services.prompts_to_image_generation import PromptToImageService
from app.config import settings
from app.utils.file_ops import ensure_dir, safe_remove
from app.database import get_db
from app.models import User as DBUser
from pathlib import Path
from uuid import uuid4

router = APIRouter(prefix="/api/prompt-to-image", tags=["Prompt to Image"])

@router.post("")
async def generate_from_prompt(
    request: Request,
    prompt: str = Form(...),
    db: Session = Depends(get_db)
):
    # --- Authentication & Credit Check ---
    email = request.cookies.get("session_user")
    if not email:
        raise HTTPException(status_code=401, detail="Please login to use this service.")
    
    user = db.query(DBUser).filter(DBUser.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    
    CREDIT_COST = 10
    if user.credits < CREDIT_COST:
        raise HTTPException(status_code=402, detail=f"Insufficient credits. This service costs {CREDIT_COST} credits.")
    # ------------------------------------

    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    ensure_dir(settings.OUTPUT_DIR)

    output_path = settings.OUTPUT_DIR / f"{uuid4().hex}.png"

    try:
        # Initialize and call service
        service = PromptToImageService()
        success = service.generate(prompt, output_path)

        if not success or not output_path.exists():
            raise HTTPException(status_code=500, detail="Image generation failed.")

        output_bytes = output_path.read_bytes()
        media_type = "image/png"

        # Deduct credits upon successful processing
        user.credits -= CREDIT_COST
        db.commit()

        return Response(content=output_bytes, media_type=media_type)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")
    finally:
        if output_path and output_path.exists():
            safe_remove(output_path)

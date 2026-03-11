from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import Response
from typing import Optional

from app.services.image_cleaner_service import clean_image

router = APIRouter(prefix='/api/image-cleaner', tags=['image-cleaner'])

@router.post('/clean')
async def clean_image_endpoint(
    file: UploadFile = File(...),
    mode: Optional[str] = Form(None),
    strength: Optional[int] = Form(None)
):
    # For now, we just pass the file, as the service doesn't use mode/strength yet
    content, media_type = await clean_image(file)
    return Response(content=content, media_type=media_type)

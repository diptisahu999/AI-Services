from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response

from app.services.image_cleaner_service import clean_image

router = APIRouter(prefix='/api/image-cleaner', tags=['image-cleaner'])


@router.post('/clean')
async def clean_image_endpoint(file: UploadFile = File(...)):
    content, media_type = await clean_image(file)
    return Response(content=content, media_type=media_type)

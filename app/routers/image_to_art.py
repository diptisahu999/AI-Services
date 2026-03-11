from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import Response
from typing import Optional
from app.services.image_to_Art import ImageToArtService
from app.config import settings
from app.utils.file_ops import ensure_dir, safe_remove
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

router = APIRouter(prefix="/api/image-to-art", tags=["Image to Art"])

@router.post("")
async def convert_to_art(
    file: UploadFile = File(...),
    mode: Optional[str] = Form(None)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

    ensure_dir(settings.TEMP_DIR)
    ensure_dir(settings.OUTPUT_DIR)

    suffix = Path(file.filename or "upload.png").suffix or ".png"
    tmp_input_path = None
    output_path = None

    try:
        content = await file.read()
        max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if len(content) > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max allowed size is {settings.MAX_UPLOAD_SIZE_MB} MB."
            )

        with NamedTemporaryFile(delete=False, suffix=suffix, dir=settings.TEMP_DIR) as tmp:
            tmp_input_path = Path(tmp.name)
            tmp.write(content)

        output_path = settings.OUTPUT_DIR / f"{uuid4().hex}{suffix}"

        # Initialize and call service
        service = ImageToArtService()
        service.process(tmp_input_path, output_path)

        if not output_path.exists():
            raise HTTPException(status_code=500, detail="Processed image was not generated.")

        output_bytes = output_path.read_bytes()
        media_type = file.content_type if file.content_type in {"image/png", "image/jpeg", "image/webp"} else "image/png"

        return Response(content=output_bytes, media_type=media_type)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image to art conversion failed: {str(e)}")
    finally:
        if tmp_input_path:
            safe_remove(tmp_input_path)
        if output_path:
            safe_remove(output_path)

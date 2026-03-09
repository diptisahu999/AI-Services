from __future__ import annotations

import importlib.util
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.config import settings
from app.utils.file_ops import ensure_dir, safe_remove


MODULE_PATH = settings.IMAGE_ENHANCEMENT_DIR / "1.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("image_enhancement_one", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def clean_image(upload: UploadFile) -> tuple[bytes, str]:
    if not upload.content_type or not upload.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload a valid image file.")

    ensure_dir(settings.TEMP_DIR)
    ensure_dir(settings.OUTPUT_DIR)

    suffix = Path(upload.filename or "upload.png").suffix or ".png"
    tmp_input_path = None
    output_path = None

    try:
        content = await upload.read()
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

        module = _load_module()

        # directly use ImgDeblur from 1.py
        img_deblur = module.ImgDeblur()
        img_deblur.process_image(str(tmp_input_path), str(output_path))

        if not output_path.exists():
            raise HTTPException(status_code=500, detail="Processed image was not generated.")

        output_bytes = output_path.read_bytes()
        media_type = (
            upload.content_type
            if upload.content_type in {"image/png", "image/jpeg", "image/webp"}
            else "image/png"
        )

        return output_bytes, media_type

    except HTTPException:
        raise
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Image cleaning failed: {exc}") from exc
    finally:
        if tmp_input_path:
            safe_remove(tmp_input_path)
        if output_path:
            safe_remove(output_path)
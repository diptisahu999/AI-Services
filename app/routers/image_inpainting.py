from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import requests
from app.database import SessionLocal
from app.models import User
from app.routers.auth import get_current_user
from app.config import settings
from PIL import Image
import io

router = APIRouter(prefix="/api/image-inpainting", tags=["Image Inpainting"])

@router.post("")
async def inpaint_image(
    file: UploadFile = File(...),
    mask_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return JSONResponse(status_code=401, content={"error": "Not authenticated"})

    if current_user.credits < 10:
        return JSONResponse(status_code=403, content={"error": "Insufficient credits"})

    try:
        # Save input files
        file_id = str(uuid.uuid4())
        input_ext = os.path.splitext(file.filename)[1] or '.png'
        input_filename = f"inpaint_input_{file_id}{input_ext}"
        mask_filename = f"inpaint_mask_{file_id}.png"
        
        input_path = settings.TEMP_DIR / input_filename
        mask_path = settings.TEMP_DIR / mask_filename
        
        # Ensure temp dir exists
        settings.TEMP_DIR.mkdir(parents=True, exist_ok=True)
        
        # Process and potentially resize images if they are too large
        try:
            input_content = await file.read()
            mask_content = await mask_file.read()
            
            img = Image.open(io.BytesIO(input_content))
            mask = Image.open(io.BytesIO(mask_content))
            
            # Use 2048 as maximum dimension for inpainting to prevent timeouts
            MAX_DIM = 2048
            if max(img.width, img.height) > MAX_DIM:
                ratio = MAX_DIM / max(img.width, img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.LANCZOS)
                mask = mask.resize(new_size, Image.NEAREST)
                
            img.save(input_path)   
            mask.save(mask_path)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image or mask file: {str(e)}")

        # Call the local lama-cleaner server
        try:
            # ALL required form fields for lama-cleaner (camelCase as per server.py)
            lama_data = {
                'ldmSteps': '20',
                'ldmSampler': 'ddim',
                'hdStrategy': 'Resize',
                'zitsWireframe': 'true',
                'hdStrategyCropMargin': '128',
                'hdStrategyCropTrigerSize': '512',
                'hdStrategyResizeLimit': '2048',
                'prompt': '',
                'negativePrompt': '',
                'useCroper': 'false',
                'croperX': '0',
                'croperY': '0',
                'croperHeight': '512',
                'croperWidth': '512',
                'sdScale': '1.0',
                'sdMaskBlur': '0',
                'sdStrength': '0.75',
                'sdSteps': '50',
                'sdGuidanceScale': '7.5',
                'sdSampler': 'ddim',
                'sdSeed': '-1',
                'sdMatchHistograms': 'false',
                'cv2Flag': 'INPAINT_NS',
                'cv2Radius': '4',
                'paintByExampleSteps': '50',
                'paintByExampleGuidanceScale': '7.5',
                'paintByExampleMaskBlur': '0',
                'paintByExampleSeed': '-1',
                'paintByExampleMatchHistograms': 'false',
                'p2pSteps': '50',
                'p2pImageGuidanceScale': '1.5',
                'p2pGuidanceScale': '7.5',
                'controlnet_conditioning_scale': '0.4',
                'controlnet_method': 'control_v11p_sd15_canny',
            }

            with open(input_path, 'rb') as img_f, open(mask_path, 'rb') as mask_f:
                lama_files = {
                    'image': (file.filename, img_f, 'image/png'),
                    'mask': ('mask.png', mask_f, 'image/png')
                }

                lama_response = requests.post(
                    "http://127.0.0.1:9080/inpaint",
                    files=lama_files,
                    data=lama_data,
                    timeout=600
                )

            if lama_response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"LaMa Engine Error: {lama_response.text}")

            # Save output
            output_filename = f"inpainted_{file_id}.png"
            output_path = settings.OUTPUT_DIR / output_filename

            with open(output_path, "wb") as out_f:
                out_f.write(lama_response.content)

        except requests.exceptions.ReadTimeout:
            raise HTTPException(status_code=504, detail="AI Engine timed out processing the image. Try with a smaller image or wait for the system to be less busy.")
        except requests.exceptions.ConnectionError:
            raise HTTPException(status_code=503, detail="AI Engine is not running. Please start lama_clener.py on port 9080.")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Inpainting processing error: {str(e)}")

        # Deduct credits
        db = SessionLocal()
        user = db.query(User).filter(User.id == current_user.id).first()
        user.credits -= 10
        db.commit()
        db.refresh(user)
        db.close()

        return JSONResponse(
            content={
                "success": True, 
                "output_url": f"/static/temp/outputs/{output_filename}",
                "credits_remaining": user.credits
            },
            headers={"X-Credits-Left": str(user.credits)}
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

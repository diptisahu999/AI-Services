import requests
import io
from PIL import Image
import os
import uuid
from typing import Optional
from app.config import settings

class PromptToImageService:
    def __init__(self):
        # API Configuration
        self.api_url = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
        # self.api_url = "https://router.huggingface.co/hf-inference/models/John6666/ras-real-anime-screencap-v1-sdxl"
        self.headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}

    def query(self, prompt: str) -> Optional[bytes]:
        try:
            payload = {"inputs": prompt}
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            if response.status_code != 200:
                print(f"Error from API (Status {response.status_code}): {response.text}")
                return None
            return response.content
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def generate(self, prompt: str, output_path: os.PathLike) -> bool:
        image_bytes = self.query(prompt)
        if not image_bytes:
            return False
            
        try:
            image = Image.open(io.BytesIO(image_bytes))
            # Ensure output directory exists (handled by the caller usually, but good to have)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            image.save(output_path)
            return True
        except Exception as e:
            print(f"Failed to process image: {e}")
            return False
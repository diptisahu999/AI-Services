import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
APP_DIR = BASE_DIR / 'app'
SERVICES_DIR = APP_DIR / 'services'
IMAGE_ENHANCEMENT_DIR = SERVICES_DIR / 'image_enhancement'

HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', '8000'))
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
MAX_UPLOAD_SIZE_MB = int(os.getenv('MAX_UPLOAD_SIZE_MB', '15'))
TEMP_DIR = Path(os.getenv('TEMP_DIR', str(BASE_DIR / 'temp')))
OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', str(TEMP_DIR / 'outputs')))

# Optional model paths. If these are not provided, the service falls back to the original absolute paths in 1.py.
GFPGAN_MODEL_PATH = os.getenv('GFPGAN_MODEL_PATH', '')
REALESRGAN_MODEL_PATH = os.getenv('REALESRGAN_MODEL_PATH', '')
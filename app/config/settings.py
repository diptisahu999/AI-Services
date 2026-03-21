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
TEMP_DIR = APP_DIR / 'static' / 'temp'
OUTPUT_DIR = TEMP_DIR / 'outputs'
# Ensure directories exist
TEMP_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Optional model paths. If these are not provided, the service falls back to the original absolute paths in 1.py.
GFPGAN_MODEL_PATH = os.getenv('GFPGAN_MODEL_PATH', '')
REALESRGAN_MODEL_PATH = os.getenv('REALESRGAN_MODEL_PATH', '')

# Hugging Face API Key
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Google Gemini API Key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
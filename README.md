# AI Service App - FastAPI

This project converts the provided UI into a FastAPI app.

## What changed
- `frontend/index.html` is now `app/templates/index.html`
- CSS and JS are served from `app/static/css` and `app/static/js`
- `image_enhancement` was moved to `app/services/image_enhancement`
- The frontend `Clean Image` button now calls `POST /api/image-cleaner/clean`
- Config reads values from environment variables using `os.getenv`, not pydantic settings

## Important note
The original `1.py` uses absolute model paths. To make the backend run correctly, set these in `.env`:
- `GFPGAN_MODEL_PATH`
- `REALESRGAN_MODEL_PATH`

The folder contents inside `app/services/image_enhancement` were kept unchanged.
The FastAPI wrapper reproduces the same enhancement flow while letting model paths come from `.env`.

## Run
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Windows PowerShell: Copy-Item .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:
- `http://127.0.0.1:8000`

## API
- `POST /api/image-cleaner/clean`
  - form field: `file`


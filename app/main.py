from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.web import router as web_router
from app.routers.image_cleaner import router as image_cleaner_router
from app.routers.image_to_art import router as image_to_art_router
from app.routers.prompt_to_image import router as prompt_to_image_router
from app.routers.image_inpainting import router as image_inpainting_router
from app.routers.auth import router as auth_router
from app.routers.blog_generator import router as blog_generator_router
from app.database import engine, Base
from app import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title='AI Service App', version='1.0.0')

# Global middleware to prevent caching of auth-sensitive pages
@app.middleware("http")
async def add_cache_control_header(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(web_router)
app.include_router(image_cleaner_router)
app.include_router(image_to_art_router)
app.include_router(prompt_to_image_router)
app.include_router(image_inpainting_router)
app.include_router(auth_router)
app.include_router(blog_generator_router)

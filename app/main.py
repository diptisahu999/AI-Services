from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.web import router as web_router
from app.routers.image_cleaner import router as image_cleaner_router


app = FastAPI(title='AI Service App', version='1.0.0')

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(web_router)
app.include_router(image_cleaner_router)

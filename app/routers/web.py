from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/image-cleaner', response_class=HTMLResponse)
async def cleaner_page(request: Request):
    return templates.TemplateResponse('cleaner.html', {'request': request})


@router.get('/image-to-art', response_class=HTMLResponse)
async def art_page(request: Request):
    return templates.TemplateResponse('art.html', {'request': request})

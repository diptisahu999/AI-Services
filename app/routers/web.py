from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User as DBUser

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')

from app.routers.auth import get_current_user

@router.get('/', response_class=HTMLResponse)
async def index(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse('index.html', {'request': request, 'user': user})

@router.get('/image-cleaner', response_class=HTMLResponse)
async def cleaner_page(request: Request, user = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse('cleaner.html', {'request': request, 'user': user})

@router.get('/image-to-art', response_class=HTMLResponse)
async def art_page(request: Request, user = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse('art.html', {'request': request, 'user': user})

@router.get('/text-to-image', response_class=HTMLResponse)
async def text_to_image_page(request: Request, user = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse('text_to_image.html', {'request': request, 'user': user})

@router.get('/pricing', response_class=HTMLResponse)
async def pricing_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse('pricing.html', {'request': request, 'user': user})

@router.get('/invite', response_class=HTMLResponse)
async def invite_page(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse('invite.html', {'request': request, 'user': user})

@router.get('/chat', response_class=HTMLResponse)
async def chat_page(request: Request, user = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse('chat.html', {'request': request, 'user': user})

@router.get('/image-inpainting', response_class=HTMLResponse)
async def inpainting_page(request: Request, user = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse('image_inpainting.html', {'request': request, 'user': user})

@router.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.get('/register', response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})

@router.get('/blog-generator', response_class=HTMLResponse)
async def blog_generator_page(request: Request, user = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse('blog_generator.html', {'request': request, 'user': user})

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User as DBUser

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')

# Helper to check if user is logged in
def get_current_user(request: Request, db: Session):
    email = request.cookies.get("session_user")
    if not email:
        return None
    return db.query(DBUser).filter(DBUser.email == email).first()

@router.get('/', response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return templates.TemplateResponse('index.html', {'request': request, 'user': user})

@router.get('/image-cleaner', response_class=HTMLResponse)
async def cleaner_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse('cleaner.html', {'request': request, 'user': user})

@router.get('/image-to-art', response_class=HTMLResponse)
async def art_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse('art.html', {'request': request, 'user': user})

@router.get('/pricing', response_class=HTMLResponse)
async def pricing_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return templates.TemplateResponse('pricing.html', {'request': request, 'user': user})

@router.get('/invite', response_class=HTMLResponse)
async def invite_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return templates.TemplateResponse('invite.html', {'request': request, 'user': user})

@router.get('/chat', response_class=HTMLResponse)
async def chat_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse('chat.html', {'request': request, 'user': user})

@router.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.get('/register', response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})

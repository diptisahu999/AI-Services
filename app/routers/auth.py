from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from hashlib import sha256
from app.database import get_db
from app.models import User as DBUser

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str):
    return sha256(password.encode()).hexdigest()

from fastapi import Request
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    email = request.cookies.get("session_user")
    if not email:
        return None
    return db.query(DBUser).filter(DBUser.email == email).first()

@router.post("/register")
async def register(response: Response, user: UserRegister, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = DBUser(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Automatically log the user in
    response.set_cookie(key="session_user", value=new_user.email, httponly=True)
    
    return {"message": "User registered successfully", "id": new_user.id}

@router.post("/login")
async def login(response: Response, user: UserLogin, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)
    
    found_user = db.query(DBUser).filter(
        DBUser.email == user.email, 
        DBUser.password == hashed_pwd
    ).first()
    
    if not found_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Set a simple session cookie (for production, use a secure token/JWT)
    response.set_cookie(key="session_user", value=found_user.email, httponly=True, path="/")
    
    return {
        "message": "Login successful", 
        "email": found_user.email,
        "name": found_user.name
    }

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("session_user", path="/")
    return response

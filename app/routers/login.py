from fastapi import APIRouter, HTTPException, Depends, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.models import User, Signup
from app.database import get_db, Base, engine, SessionLocal
import datetime

Base.metadata.create_all(bind = engine)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/signup", response_class=HTMLResponse, status_code=200)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/add_user", response_class=HTMLResponse, status_code=200)
async def add_new_user(
    request: Request,
    username: str =Form(...),
    password: str = Form(...),
    email_id: str = Form(...),
    db: Session = Depends(get_db)
    ):
    user = db.query(Signup).filter(Signup.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    try:
        hashed_password = bcrypt.hash(password)
        new_user = Signup(
            username=username,
            password=hashed_password,
            email_id=email_id,
            register_date=datetime.datetime.now()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return RedirectResponse("/signup", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error occurred: {e}")


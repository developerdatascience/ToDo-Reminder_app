from fastapi import APIRouter, HTTPException, Depends, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import ToDo
from app.database import get_db, Base, engine, SessionLocal
from app.schemas import ToDoCreate, ToDoResponse
import datetime


Base.metadata.create_all(bind = engine)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/todo", response_class=HTMLResponse, status_code=201)
async def get_task(request: Request, name="get_task", db: Session = Depends(get_db)):
    users = db.query(ToDo).all()
    title = "To-Do Application"
    return templates.TemplateResponse(
        "todo.html", 
        {'request': request, "users": users, "title": title})

@router.get("/todo/add_task", response_class=HTMLResponse, status_code=201)
async def add_task(request: Request):
    return templates.TemplateResponse("addtask.html", {"request": request})

@router.post("/todo/create_task/", response_class=HTMLResponse, status_code=201)
def create_todo(request: Request, 
                task_name: str = Form(...),
                start_date: str = Form(...),
                status: str = Form(...),
                db: Session = Depends(get_db)):
    try:
        new_task = ToDo(
            task_name=task_name,
            start_date=datetime.datetime.strptime(start_date, "%Y-%m-%d").date(),
            status=status
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return RedirectResponse(url= request.app.url_path_for('get_task'), status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Task not created. Error: {e}")

@router.get("/todo/update/{task_id}", response_class=HTMLResponse, status_code=200)
async def edit_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(ToDo).filter(ToDo.id == task_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Task not found")
        return templates.TemplateResponse("update.html", {"request": request, "task": todo})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the task: {e}")

@router.post("/update/{task_id}", response_class=HTMLResponse, status_code=201)
async def update_task(request: Request, 
                      task_id: int, 
                      task_name: str = Form(...),
                      start_date: str = Form(...), 
                      status: str = Form(...), 
                      db: Session = Depends(get_db)):
    try:
        todo = db.query(ToDo).filter(ToDo.id == task_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Task not found")
        todo.task_name = task_name
        todo.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        todo.status = status
        db.commit()
        return RedirectResponse(url="/todo", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the task: {e}")


@router.get("/delete/{task_id}", response_class=HTMLResponse, status_code=200)
async def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(ToDo).filter(ToDo.id == task_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Task not found")
        db.delete(todo)
        db.commit()
        return RedirectResponse(url="/todo", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the task: {e}")



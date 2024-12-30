from fastapi import APIRouter, HTTPException, Depends, requests
from sqlalchemy.orm import Session
from app.models import ToDo
from app.database import get_db, Base, engine, SessionLocal
from app.schemas import ToDoCreate, ToDoResponse

Base.metadata.create_all(bind = engine)

router = APIRouter()

@router.post("/", status_code=201)
async def get_task(db: Session = Depends(get_db)):
    return db.query(ToDo).all()


@router.post("/create_task", status_code=201)
def create_todo(task: ToDoCreate, db: Session = Depends(get_db)):
    try:
        db = SessionLocal()
        new_task = ToDo(
            task_name=task.task_name,
            start_date=task.start_date,
            status=task.status
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return {"message": "Task created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Task not created")


@router.put("/update/{task_id}", status_code=201)
async def update_task(task_id: int, task: ToDoResponse, db: Session = Depends(get_db)):
    try:
        todo = db.query(ToDo).filter(ToDo.id == task_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Task not found")
        todo.task_name = task.task_name
        todo.start_date = task.start_date
        todo.status = task.status
        db.commit()
        return {"message": "Task updated successfully"}
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while updating the task")


@router.delete("/delete/{task_id}", status_code=200)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(ToDo).filter(ToDo.id == task_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Task not found")
        db.delete(todo)
        db.commit()
        return {"message": "Task deleted successfully"}
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while deleting the task")

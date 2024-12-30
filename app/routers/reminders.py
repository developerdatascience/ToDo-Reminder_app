from fastapi import APIRouter, HTTPException, Depends, requests
from sqlalchemy.orm import Session
from app.models import Reminder
from app.database import get_db, Base, engine, SessionLocal
from app.schemas import CreateReminder

Base.metadata.create_all(bind = engine)
router = APIRouter()

@router.post("/", status_code=201)
def get_reminders(db: Session = Depends(get_db)):
    return db.query(Reminder).all()

@router.post("/create_reminder", status_code=201)
async def create_reminders(reminder: CreateReminder, db: Session = Depends(get_db)):
    try:
        db = SessionLocal()
        new_reminder = Reminder(
            task_name = reminder.task_name,
            contact_name = reminder.contact_name,
            contact_number = reminder.contact_number,
            last_service_date = reminder.last_service_date,
            next_service_date = reminder.next_service_date
        )
        db.add(new_reminder)
        db.commit()
        db.refresh(new_reminder)
        return {"message": "Reminder created successfully"}
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Reminder not created")

@router.put("/update/{reminder_id}", status_code=201)
async def update_reminder(reminder_id: int, reminder: CreateReminder, db: Session= Depends(get_db)):
    try:
        reminder_name = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not reminder_name:
            raise HTTPException(status_code=404, detail="Reminder not found")
        
        reminder_name.task_name = reminder.task_name
        reminder_name.contact_name = reminder.contact_name
        reminder_name.contact_number = reminder.contact_number
        reminder_name.last_service_date = reminder.last_service_date
        reminder_name.next_service_date = reminder.next_service_date
        db.commit()
        return {"message": "Reminder updated successfully"}
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="An error occured while updating the reminder")

@router.delete("/delete/{reminder_id}", status_code=201)
async def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    try:
        reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not reminder:
            raise HTTPException(status_code=404, detail="Reminder not found")
        db.delete(reminder)
        db.commit()
        return {"message": f"{reminder_id} Reminder deleted successfully"}
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="An error occured while deleting the reminder")


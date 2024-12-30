from pydantic import BaseModel
from datetime import date

class ToDoCreate(BaseModel):
    task_name: str
    start_date: date
    status: str

    class Config:
        orm_mode = True  # Enable ORM mode to work with SQLAlchemy models

class ToDoResponse(BaseModel):
    task_name: str
    start_date: date
    status: str

    class Config:
        orm_mode = True


class CreateReminder(BaseModel):
    task_name: str
    contact_name: str
    contact_number: str
    last_service_date: date
    next_service_date: date

    class Config:
        orm_mode = True
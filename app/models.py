from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class ToDo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)
    start_date = Column(Date)
    status = Column(String)


class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)
    contact_name = Column(String)
    contact_number = Column(String)
    last_service_date = Column(Date)
    next_service_date = Column(Date)

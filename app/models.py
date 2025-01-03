from sqlalchemy import Column, Integer, String, Date, DateTime
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

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    first_login = Column(String, nullable=False)
    login_time = Column(DateTime, nullable=False)
    logout_time = Column(DateTime, nullable=False)
    time_logged_in = Column(Integer, nullable=True)

class Signup(Base):
    __tablename__ = "signup"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email_id = Column(String, nullable=False)
    register_date = Column(DateTime, nullable=False)

from fastapi import FastAPI
from .routers import todo, reminders
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(todo.router, prefix="/todo", tags=["todo"])
app.include_router(reminders.router, prefix="/reminder", tags=["reminder"])
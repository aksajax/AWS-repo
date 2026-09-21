from fastapi import FastAPI

from app.database.database import Base, engine
from app.models import task, user
from app.routes.auth import router as auth_router
from app.routes.tasks import router as task_router
from app.routes.upload import router as upload_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FastAPI AWS Project",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(task_router)
app.include_router(upload_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to FastAPI AWS Project"
    }
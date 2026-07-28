from fastapi import FastAPI
from api import routes
from db.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OjaSuper API",
    description="Autonomous Offline AI Business Operating System",
    version="1.0.0"
)

app.include_router(routes.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to OjaSuper API"}

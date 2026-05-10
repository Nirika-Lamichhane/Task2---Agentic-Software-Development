from fastapi import FastAPI

from app.db.database import engine, Base
from app.models import models
from app.routers.router import router
from app.config.logger import get_logger

logger = get_logger("main")

# Create FastAPI app
app = FastAPI(title="ClassicModels Customer API", version="0.1.0")

# Database initialization
Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the ClassicModels Customer API"}

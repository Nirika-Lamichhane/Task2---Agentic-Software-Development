from fastapi import FastAPI

import models
import database
from router import router
from logger import get_logger

logger = get_logger("main")

# Create FastAPI app
app = FastAPI(title="ClassicModels Customer API", version="0.1.0")

# Database initialization
models.Base.metadata.create_all(bind=database.engine)

app.include_router(router)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the ClassicModels Customer API"}

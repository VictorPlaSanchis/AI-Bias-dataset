from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="AI Bias Detector")
app.include_router(router, prefix="/api")

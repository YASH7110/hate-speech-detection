from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import twitter, youtube, prediction
from app.utils.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Multilingual Hate Speech Detection API",
    description="Real-time hate speech detection for Twitter and YouTube comments",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(twitter.router, prefix="/api/twitter", tags=["Twitter"])
app.include_router(youtube.router, prefix="/api/youtube", tags=["YouTube"])
app.include_router(prediction.router, prefix="/api/predict", tags=["Prediction"])

@app.get("/")
async def root():
    return {
        "message": "Multilingual Hate Speech Detection API",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )

from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.comment import CommentAnalysis
from app.services.youtube_service import get_youtube_service, YouTubeService
from app.services.ml_service import get_ml_service, MLService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/video", response_model=list[CommentAnalysis])
async def get_video_comments(
    video_url: str = Query(..., description="YouTube video URL or ID"),
    max_results: int = Query(100, ge=10, le=100),
    youtube_service: YouTubeService = Depends(get_youtube_service),
    ml_service: MLService = Depends(get_ml_service)
):
    """Get comments from a YouTube video and analyze for hate speech"""
    try:
        # Fetch comments
        comments = await youtube_service.get_video_comments(video_url, max_results)
        
        # Analyze each comment
        analyses = []
        for comment in comments:
            prediction = await ml_service.analyze_text(comment.text)
            analyses.append(CommentAnalysis(comment=comment, prediction=prediction))
        
        return analyses
    except Exception as e:
        logger.error(f"Error fetching video comments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/channel/{channel_id}", response_model=list[CommentAnalysis])
async def get_channel_comments(
    channel_id: str,
    max_results: int = Query(100, ge=10, le=100),
    youtube_service: YouTubeService = Depends(get_youtube_service),
    ml_service: MLService = Depends(get_ml_service)
):
    """Get comments from a YouTube channel and analyze for hate speech"""
    try:
        # Fetch comments
        comments = await youtube_service.get_channel_comments(channel_id, max_results)
        
        # Analyze each comment
        analyses = []
        for comment in comments:
            prediction = await ml_service.analyze_text(comment.text)
            analyses.append(CommentAnalysis(comment=comment, prediction=prediction))
        
        return analyses
    except Exception as e:
        logger.error(f"Error fetching channel comments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

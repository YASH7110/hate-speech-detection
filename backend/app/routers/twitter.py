from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.comment import CommentAnalysis
from app.services.twitter_service import get_twitter_service, TwitterService
from app.services.ml_service import get_ml_service, MLService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/search", response_model=list[CommentAnalysis])
async def search_tweets(
    keyword: str = Query(..., description="Search keyword"),
    max_results: int = Query(100, ge=10, le=100),
    twitter_service: TwitterService = Depends(get_twitter_service),
    ml_service: MLService = Depends(get_ml_service)
):
    """Search tweets by keyword and analyze for hate speech"""
    try:
        # Fetch tweets
        comments = await twitter_service.get_tweets_by_keyword(keyword, max_results)
        
        # Analyze each comment
        analyses = []
        for comment in comments:
            prediction = await ml_service.analyze_text(comment.text)
            analyses.append(CommentAnalysis(comment=comment, prediction=prediction))
        
        return analyses
    except Exception as e:
        logger.error(f"Error searching tweets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{username}", response_model=list[CommentAnalysis])
async def get_user_tweets(
    username: str,
    max_results: int = Query(100, ge=10, le=100),
    twitter_service: TwitterService = Depends(get_twitter_service),
    ml_service: MLService = Depends(get_ml_service)
):
    """Get tweets from a specific user and analyze for hate speech"""
    try:
        # Fetch user tweets
        comments = await twitter_service.get_user_tweets(username, max_results)
        
        # Analyze each comment
        analyses = []
        for comment in comments:
            prediction = await ml_service.analyze_text(comment.text)
            analyses.append(CommentAnalysis(comment=comment, prediction=prediction))
        
        return analyses
    except Exception as e:
        logger.error(f"Error fetching user tweets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

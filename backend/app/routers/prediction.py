# from fastapi import APIRouter, HTTPException, Depends
# from app.schemas.comment import (
#     PredictionRequest,
#     PredictionResponse,
#     BatchAnalysisRequest,
#     BatchAnalysisResponse
# )
# from app.services.ml_service import get_ml_service, MLService
# import logging

# logger = logging.getLogger(__name__)
# router = APIRouter()

# @router.post("/single", response_model=PredictionResponse)
# async def predict_single(
#     request: PredictionRequest,
#     ml_service: MLService = Depends(get_ml_service)
# ):
#     """Analyze a single text for hate speech"""
#     try:
#         result = await ml_service.analyze_text(request.text)
#         return result
#     except Exception as e:
#         logger.error(f"Error in prediction: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/batch", response_model=BatchAnalysisResponse)
# async def predict_batch(
#     request: BatchAnalysisRequest,
#     ml_service: MLService = Depends(get_ml_service)
# ):
#     """Analyze multiple texts for hate speech"""
#     try:
#         results = await ml_service.analyze_batch(request.comments)
        
#         # Calculate statistics
#         hate_speech_count = sum(1 for r in results if r.classification == "hate_speech")
#         offensive_count = sum(1 for r in results if r.classification == "offensive")
#         neutral_count = sum(1 for r in results if r.classification == "neutral")
        
#         return BatchAnalysisResponse(
#             results=results,
#             total_analyzed=len(results),
#             hate_speech_count=hate_speech_count,
#             offensive_count=offensive_count,
#             neutral_count=neutral_count
#         )
#     except Exception as e:
#         logger.error(f"Error in batch prediction: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException, Depends
from app.schemas.comment import (
    PredictionRequest,
    PredictionResponse,
    BatchAnalysisRequest,
    BatchAnalysisResponse,
    FeedbackRequest,
    FeedbackResponse
)
from app.services.ml_service import get_ml_service, MLService
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/single", response_model=PredictionResponse)
async def predict_single(
    request: PredictionRequest,
    ml_service: MLService = Depends(get_ml_service)
):
    """Analyze a single text for hate speech"""
    try:
        result = await ml_service.analyze_text(request.text)
        return result
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=BatchAnalysisResponse)
async def predict_batch(
    request: BatchAnalysisRequest,
    ml_service: MLService = Depends(get_ml_service)
):
    """Analyze multiple texts for hate speech"""
    try:
        results = await ml_service.analyze_batch(request.comments)
        
        # Calculate statistics
        hate_speech_count = sum(1 for r in results if r.classification == "hate_speech")
        offensive_count = sum(1 for r in results if r.classification == "offensive")
        neutral_count = sum(1 for r in results if r.classification == "neutral")
        
        return BatchAnalysisResponse(
            results=results,
            total_analyzed=len(results),
            hate_speech_count=hate_speech_count,
            offensive_count=offensive_count,
            neutral_count=neutral_count
        )
    except Exception as e:
        logger.error(f"Error in batch prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    ml_service: MLService = Depends(get_ml_service)
):
    """
    Submit user feedback for a prediction.
    This helps improve model accuracy over time.
    """
    try:
        # Create feedback storage directory
        feedback_dir = "feedback_data"
        os.makedirs(feedback_dir, exist_ok=True)
        
        # Prepare feedback data
        feedback_data = {
            "id": request.comment_id,
            "text": request.text,
            "predicted_classification": request.predicted_classification,
            "user_classification": request.user_classification,
            "is_correct": request.is_correct,
            "confidence": request.confidence,
            "timestamp": datetime.now().isoformat(),
            "language": request.language
        }
        
        # Append to feedback file
        feedback_file = os.path.join(feedback_dir, "user_feedback.jsonl")
        with open(feedback_file, 'a') as f:
            f.write(json.dumps(feedback_data) + '\n')
        
        logger.info(f"Feedback recorded: {feedback_data['id']}")
        
        return FeedbackResponse(
            success=True,
            message="Thank you for your feedback! This helps improve our model."
        )
        
    except Exception as e:
        logger.error(f"Error recording feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

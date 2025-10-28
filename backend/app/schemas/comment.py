# from pydantic import BaseModel, Field
# from typing import Optional, Literal
# from datetime import datetime

# class Comment(BaseModel):
#     id: str
#     text: str
#     author: str
#     timestamp: datetime
#     platform: Literal["twitter", "youtube"]
    
# class PredictionRequest(BaseModel):
#     text: str
    
# class PredictionResponse(BaseModel):
#     text: str
#     language: str
#     language_confidence: float
#     hate_speech: bool
#     classification: Literal["hate_speech", "offensive", "neutral"]
#     confidence: float
    
# class CommentAnalysis(BaseModel):
#     comment: Comment
#     prediction: PredictionResponse
    
# class BatchAnalysisRequest(BaseModel):
#     comments: list[str]
    
# class BatchAnalysisResponse(BaseModel):
#     results: list[PredictionResponse]
#     total_analyzed: int
#     hate_speech_count: int
#     offensive_count: int
#     neutral_count: int

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class Comment(BaseModel):
    id: str
    text: str
    author: str
    timestamp: datetime
    platform: Literal["twitter", "youtube"]
    
class PredictionRequest(BaseModel):
    text: str
    
class PredictionResponse(BaseModel):
    text: str
    language: str
    language_confidence: float
    hate_speech: bool
    classification: Literal["hate_speech", "offensive", "neutral"]
    confidence: float
    
class CommentAnalysis(BaseModel):
    comment: Comment
    prediction: PredictionResponse
    
class BatchAnalysisRequest(BaseModel):
    comments: list[str]
    
class BatchAnalysisResponse(BaseModel):
    results: list[PredictionResponse]
    total_analyzed: int
    hate_speech_count: int
    offensive_count: int
    neutral_count: int

# ⬇️⬇️⬇️ ADD THESE TWO CLASSES BELOW ⬇️⬇️⬇️

class FeedbackRequest(BaseModel):
    comment_id: str
    text: str
    predicted_classification: str
    user_classification: Optional[str] = None
    is_correct: bool
    confidence: float
    language: str


class FeedbackResponse(BaseModel):
    success: bool
    message: str

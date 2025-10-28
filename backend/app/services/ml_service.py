from app.models.hate_speech_model import get_hate_speech_classifier
from app.models.language_detector import get_language_detector
from app.schemas.comment import PredictionResponse
from app.utils.config import settings
import logging

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.hate_speech_model = get_hate_speech_classifier(
            settings.HATE_SPEECH_MODEL_PATH,
            settings.VECTORIZER_PATH
        )
        self.language_detector = get_language_detector(settings.FASTTEXT_MODEL_PATH)
    
    async def analyze_text(self, text: str) -> PredictionResponse:
        """Analyze a single text for language and hate speech"""
        try:
            # Detect language
            language, lang_confidence = self.language_detector.detect(text)
            
            # Classify hate speech
            classification, confidence = self.hate_speech_model.predict(text)
            
            # Determine if hate speech
            hate_speech = classification == "hate_speech"
            
            return PredictionResponse(
                text=text,
                language=language,
                language_confidence=lang_confidence,
                hate_speech=hate_speech,
                classification=classification,
                confidence=confidence
            )
        except Exception as e:
            logger.error(f"Error analyzing text: {e}")
            raise
    
    async def analyze_batch(self, texts: list[str]) -> list[PredictionResponse]:
        """Analyze multiple texts"""
        results = []
        for text in texts:
            try:
                result = await self.analyze_text(text)
                results.append(result)
            except Exception as e:
                logger.error(f"Error analyzing text: {e}")
                continue
        return results

# Singleton instance
_ml_service = None

def get_ml_service() -> MLService:
    global _ml_service
    if _ml_service is None:
        _ml_service = MLService()
    return _ml_service

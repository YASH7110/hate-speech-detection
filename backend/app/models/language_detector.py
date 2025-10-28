from fasttext import load_model
import os
import logging
import urllib.request

logger = logging.getLogger(__name__)


class LanguageDetector:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load FastText language detection model"""
        try:
            if not os.path.exists(self.model_path):
                logger.warning(f"FastText model not found at {self.model_path}")
                logger.info("Downloading FastText language detection model...")
                self._download_model()
            
            # Load FastText model directly
            self.model = load_model(self.model_path)
            logger.info("FastText language detector loaded successfully")
        except Exception as e:
            logger.error(f"Error loading language detector: {e}")
            raise
    
    def _download_model(self):
        """Download FastText pretrained model"""
        url = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        urllib.request.urlretrieve(url, self.model_path)
        logger.info("FastText model downloaded successfully")
    
    def detect(self, text: str) -> tuple:
        """
        Detect language of text
        Returns: (language_code, confidence)
        """
        try:
            if not text or len(text.strip()) < 3:
                return ("en", 1.0)
            
            # FastText predict returns (labels, probabilities)
            predictions = self.model.predict(text.replace('\n', ' '), k=1)
            lang_code = predictions[0][0].replace('__label__', '')
            confidence = float(predictions[1][0])
            
            return (lang_code, confidence)
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return ("en", 0.0)
    
    def detect_multiple(self, texts: list) -> list:
        """Detect language for multiple texts"""
        return [self.detect(text) for text in texts]


# Singleton instance
_language_detector = None


def get_language_detector(model_path: str = "trained_models/lid.176.bin") -> LanguageDetector:
    global _language_detector
    if _language_detector is None:
        _language_detector = LanguageDetector(model_path)
    return _language_detector


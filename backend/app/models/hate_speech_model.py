import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
import re
import logging

logger = logging.getLogger(__name__)

class HateSpeechClassifier:
    def __init__(self, model_path: str = None, vectorizer_path: str = None):
        self.model = None
        self.vectorizer = None
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.label_map = {0: "hate_speech", 1: "offensive", 2: "neutral"}
        
        if model_path and vectorizer_path:
            self.load_model()
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for classification"""
        # Convert to lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove user mentions
        text = re.sub(r'@\w+', '', text)
        # Remove hashtags
        text = re.sub(r'#\w+', '', text)
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def load_model(self):
        """Load trained model and vectorizer"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(self.vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            logger.info("Hate speech model loaded successfully")
        except FileNotFoundError:
            logger.error("Model files not found. Please train the model first.")
            raise
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def save_model(self):
        """Save trained model and vectorizer"""
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        with open(self.vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        logger.info("Model saved successfully")
    
    def predict(self, text: str) -> tuple[str, float]:
        """
        Predict hate speech classification
        Returns: (classification, confidence)
        """
        if self.model is None or self.vectorizer is None:
            raise ValueError("Model not loaded. Please load or train the model first.")
        
        # Preprocess
        processed_text = self.preprocess_text(text)
        
        # Vectorize
        features = self.vectorizer.transform([processed_text])
        
        # Predict
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = float(np.max(probabilities))
        
        classification = self.label_map[prediction]
        
        return classification, confidence
    
    def predict_batch(self, texts: list[str]) -> list[tuple[str, float]]:
        """Predict for multiple texts"""
        return [self.predict(text) for text in texts]
    
    def is_hate_speech(self, text: str, threshold: float = 0.5) -> bool:
        """Check if text is hate speech"""
        classification, confidence = self.predict(text)
        return classification == "hate_speech" and confidence >= threshold

# Singleton instance
_hate_speech_classifier = None

def get_hate_speech_classifier(
    model_path: str = "trained_models/hate_speech_classifier.pkl",
    vectorizer_path: str = "trained_models/vectorizer.pkl"
) -> HateSpeechClassifier:
    global _hate_speech_classifier
    if _hate_speech_classifier is None:
        _hate_speech_classifier = HateSpeechClassifier(model_path, vectorizer_path)
    return _hate_speech_classifier

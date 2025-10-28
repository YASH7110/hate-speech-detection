import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import re
import os
from datasets import load_dataset

print("Loading dataset...")
dataset = load_dataset("tdavidson/hate_speech_offensive")
df = pd.DataFrame(dataset['train'])

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

print("Preprocessing...")
df['clean_text'] = df['tweet'].apply(preprocess_text)
df['label'] = df['class']
df = df[df['clean_text'].str.strip() != '']

X = df['clean_text']
y = df['label']

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Extracting TF-IDF features...")
vectorizer = TfidfVectorizer(
    max_features=5000,
    min_df=5,
    max_df=0.8,
    ngram_range=(1, 2),
    stop_words='english'
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Training model... (this will take 5-10 minutes)")
clf = MLPClassifier(
    hidden_layer_sizes=(128, 64, 32),
    activation='relu',
    solver='adam',
    alpha=0.0001,
    batch_size=256,
    learning_rate='adaptive',
    max_iter=50,
    random_state=42,
    verbose=True,
    early_stopping=True,
    validation_fraction=0.1
)

clf.fit(X_train_vec, y_train)

print("\nEvaluating...")
y_pred = clf.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")

os.makedirs('trained_models', exist_ok=True)

with open('trained_models/hate_speech_classifier.pkl', 'wb') as f:
    pickle.dump(clf, f)

with open('trained_models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("\n✅ Model retrained and saved successfully!")


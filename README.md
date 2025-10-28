# 🚫 Hate Speech Detection System

A full-stack multilingual hate speech detection application using Machine Learning, FastAPI, and React.

## 🌟 Features

- **Real-time Analysis**: Analyze comments from Twitter and YouTube
- **Manual Testing**: Test individual comments instantly
- **Multilingual Support**: Detects hate speech in multiple languages
- **User Feedback**: Improve model accuracy with user feedback
- **Beautiful UI**: Modern interface with animations
- **ML Model**: 88.88% accuracy neural network classifier

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **scikit-learn**: Machine learning models
- **FastText**: Language detection
- **Python 3.10**

### Frontend
- **React + Vite**: Fast modern frontend
- **TailwindCSS**: Styling
- **Lucide Icons**: Beautiful icons
- **Axios**: API calls

## 📦 Installation

### Backend Setup

cd backend
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload 
### Frontend Setup

cd frontend
npm install
npm run dev
## 🔑 Environment Variables

Create `.env` file in `backend/`:

YOUTUBE_API_KEY=your_youtube_api_key
TWITTER_BEARER_TOKEN=your_twitter_bearer_token 
## 🚀 Usage

1. Start backend server (port 8000)
2. Start frontend server (port 5173)
3. Open http://localhost:5173
4. Analyze comments from YouTube/Twitter or test manually

## 📊 Model Performance

- **Accuracy**: 88.88%
- **Dataset**: Davidson Hate Speech Dataset
- **Architecture**: Neural Network (MLP Classifier)

## 🤝 Contributing

Contributions welcome! Please open an issue first.

## 📄 License

MIT License

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)


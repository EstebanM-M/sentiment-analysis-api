# Sentiment Analysis API 🎭

A production-ready sentiment analysis API built with FastAPI and Transformers, featuring real-time text analysis, historical data persistence, and RESTful endpoints.

## ✨ Features

- **State-of-the-art NLP**: Powered by pre-trained Transformer models (DistilBERT)
- **Fast API**: Built with FastAPI for high performance and automatic documentation
- **Data Persistence**: PostgreSQL database for analysis history
- **Batch Processing**: Analyze multiple texts efficiently
- **Testing**: Comprehensive test suite with >70% coverage
- **Production Ready**: Docker support and deployment configurations

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL (or use Docker Compose)
- pip or conda

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/EstebanM-M/sentiment-analysis-api.git
cd sentiment-analysis-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -e .
# Or for development:
pip install -e ".[dev]"
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the API**
```bash
uvicorn api.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 📊 API Endpoints

### Analyze Sentiment
```bash
POST /api/v1/analyze
{
  "text": "I love this product! It's amazing."
}

Response:
{
  "text": "I love this product! It's amazing.",
  "label": "POSITIVE",
  "score": 0.9987,
  "timestamp": "2025-01-03T16:30:00Z"
}
```

### Batch Analysis
```bash
POST /api/v1/batch-analyze
{
  "texts": ["Great service!", "Terrible experience", "It's okay"]
}

Response:
{
  "total_analyzed": 3,
  "results": [...],
  "processing_time_ms": 125.5
}
```

### Health Check
```bash
GET /api/v1/health

Response:
{
  "status": "healthy",
  "model_loaded": true,
  "model_info": {...}
}
```

### Model Info
```bash
GET /api/v1/model-info
```

### Analysis History
```bash
GET /api/v1/history?page=1&page_size=20&label=POSITIVE

Response:
{
  "total": 150,
  "page": 1,
  "page_size": 20,
  "analyses": [...]
}
```

### Statistics
```bash
GET /api/v1/stats?days=7

Response:
{
  "total_analyses": 150,
  "positive_count": 120,
  "negative_count": 30,
  "positive_percentage": 80.0,
  "negative_percentage": 20.0,
  "average_score": 0.89,
  "average_processing_time_ms": 45.2
}
```

### Timeline Statistics
```bash
GET /api/v1/stats/timeline?days=7

Response:
{
  "dates": {
    "2025-01-01": 10,
    "2025-01-02": 15,
    ...
  },
  "total": 100
}
```

### Search
```bash
GET /api/v1/search?q=product&limit=50
```

## 🏗️ Project Structure

```
sentiment-analysis-api/
├── src/
│   ├── api/              # FastAPI application
│   ├── models/           # ML models and inference
│   ├── database/         # Database models and connection
│   └── utils/            # Utility functions
├── tests/                # Test suite
├── notebooks/            # Jupyter notebooks for exploration
├── setup.py              # Package configuration
└── requirements.txt      # Dependencies
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

## 🐳 Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# API will be available at http://localhost:8000
```

## 📈 Model Details

- **Base Model**: distilbert-base-uncased-finetuned-sst-2-english
- **Task**: Binary sentiment classification (Positive/Negative)
- **Framework**: HuggingFace Transformers
- **Performance**: ~95% accuracy on SST-2 benchmark

## 🚀 Deployment

### Production Deployment

This API is production-ready and can be deployed to:

**Option 1: Render (Recommended - Free)**
- See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions
- Free tier includes PostgreSQL database
- Auto-deploy from GitHub
- HTTPS automatic

**Option 2: Railway (Alternative)**
- See [DEPLOYMENT_RAILWAY.md](DEPLOYMENT_RAILWAY.md) for instructions
- $5/month free credit
- Better performance than Render free tier

**Live Demo:** Coming soon

### Quick Deploy to Render

1. Fork this repository
2. Sign up at [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
6. Add PostgreSQL database
7. Connect DATABASE_URL
8. Deploy!

See full guide in [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 🛠️ Tech Stack

- **API Framework**: FastAPI
- **ML Framework**: PyTorch + Transformers
- **Database**: PostgreSQL + SQLAlchemy
- **Testing**: pytest
- **Deployment**: Docker, Render/Railway

## 📝 Development Roadmap

- [x] Core sentiment analysis
- [x] FastAPI endpoints
- [x] PostgreSQL integration
- [x] Testing suite
- [ ] Multi-language support (Spanish)
- [ ] Fine-tuning on custom datasets
- [ ] Analytics dashboard
- [ ] Redis caching

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details.

## 👨‍💻 Author

**Esteban**
- Electronic Engineer transitioning to ML/AI
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

Built with ❤️ as part of my ML/AI portfolio

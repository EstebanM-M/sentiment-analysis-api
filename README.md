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
git clone https://github.com/yourusername/sentiment-analysis-api.git
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
```

### Batch Analysis
```bash
POST /api/v1/batch-analyze
{
  "texts": ["Great service!", "Terrible experience", "It's okay"]
}
```

### Get Analysis History
```bash
GET /api/v1/history?limit=10
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

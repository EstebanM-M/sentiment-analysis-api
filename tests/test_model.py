"""
Unit tests for the sentiment analysis model
"""

import pytest
from models.sentiment_model import SentimentAnalyzer, get_analyzer


class TestSentimentAnalyzer:
    """Test suite for SentimentAnalyzer class"""
    
    @pytest.fixture(scope="class")
    def analyzer(self):
        """Create analyzer instance for tests"""
        return SentimentAnalyzer()
    
    def test_initialization(self, analyzer):
        """Test that analyzer initializes correctly"""
        assert analyzer is not None
        assert analyzer.model_name == "distilbert-base-uncased-finetuned-sst-2-english"
        assert analyzer.pipeline is not None
    
    def test_analyze_positive_sentiment(self, analyzer):
        """Test analysis of positive text"""
        text = "I love this product! It's amazing!"
        result = analyzer.analyze(text)
        
        assert "label" in result
        assert "score" in result
        assert "text" in result
        assert result["text"] == text
        assert result["label"] == "POSITIVE"
        assert 0 <= result["score"] <= 1
    
    def test_analyze_negative_sentiment(self, analyzer):
        """Test analysis of negative text"""
        text = "This is terrible. Worst experience ever."
        result = analyzer.analyze(text)
        
        assert result["label"] == "NEGATIVE"
        assert 0 <= result["score"] <= 1
    
    def test_analyze_empty_text(self, analyzer):
        """Test that empty text raises ValueError"""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            analyzer.analyze("")
    
    def test_analyze_whitespace_only(self, analyzer):
        """Test that whitespace-only text raises ValueError"""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            analyzer.analyze("   ")
    
    def test_analyze_batch(self, analyzer):
        """Test batch analysis"""
        texts = [
            "Great product!",
            "Terrible service",
            "It's okay"
        ]
        results = analyzer.analyze_batch(texts)
        
        assert len(results) == 3
        assert all("label" in r for r in results)
        assert all("score" in r for r in results)
        assert all("text" in r for r in results)
    
    def test_analyze_batch_empty_list(self, analyzer):
        """Test that empty batch raises ValueError"""
        with pytest.raises(ValueError, match="Texts list cannot be empty"):
            analyzer.analyze_batch([])
    
    def test_analyze_batch_all_empty_texts(self, analyzer):
        """Test that batch with all empty texts raises ValueError"""
        with pytest.raises(ValueError, match="All texts are empty"):
            analyzer.analyze_batch(["", "  ", "\n"])
    
    def test_analyze_with_all_scores(self, analyzer):
        """Test analysis with all scores returned"""
        text = "This is great!"
        result = analyzer.analyze(text, return_all_scores=True)
        
        assert "predictions" in result
        assert isinstance(result["predictions"], list)
        assert len(result["predictions"]) > 0
        assert all("label" in pred and "score" in pred for pred in result["predictions"])
    
    def test_get_model_info(self, analyzer):
        """Test getting model information"""
        info = analyzer.get_model_info()
        
        assert "model_name" in info
        assert "device" in info
        assert "cache_dir" in info
        assert info["model_name"] == "distilbert-base-uncased-finetuned-sst-2-english"


class TestGetAnalyzer:
    """Test suite for get_analyzer singleton function"""
    
    def test_get_analyzer_returns_instance(self):
        """Test that get_analyzer returns an instance"""
        analyzer = get_analyzer()
        assert isinstance(analyzer, SentimentAnalyzer)
    
    def test_get_analyzer_singleton(self):
        """Test that get_analyzer returns the same instance"""
        analyzer1 = get_analyzer()
        analyzer2 = get_analyzer()
        assert analyzer1 is analyzer2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

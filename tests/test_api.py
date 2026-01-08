"""
API endpoint tests
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app

# Create test client
client = TestClient(app)


class TestRootEndpoint:
    """Tests for root endpoint"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data


class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_check(self):
        """Test health check returns healthy status"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["model_loaded"] is True
        assert "model_info" in data
        assert "timestamp" in data
    
    def test_model_info_endpoint(self):
        """Test model info endpoint"""
        response = client.get("/api/v1/model-info")
        assert response.status_code == 200
        
        data = response.json()
        assert "model" in data
        assert "capabilities" in data
        assert "performance" in data


class TestAnalyzeEndpoint:
    """Tests for single text analysis endpoint"""
    
    def test_analyze_positive_sentiment(self):
        """Test analysis of positive text"""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "I love this product! It's amazing!"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "text" in data
        assert "label" in data
        assert "score" in data
        assert "timestamp" in data
        assert data["label"] == "POSITIVE"
        assert 0 <= data["score"] <= 1
    
    def test_analyze_negative_sentiment(self):
        """Test analysis of negative text"""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "This is terrible. Worst experience ever."}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["label"] == "NEGATIVE"
        assert 0 <= data["score"] <= 1
    
    def test_analyze_with_all_scores(self):
        """Test analysis with return_all_scores=true"""
        response = client.post(
            "/api/v1/analyze",
            json={
                "text": "This is great!",
                "return_all_scores": True
            }
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "predictions" in data
        assert isinstance(data["predictions"], list)
        assert len(data["predictions"]) > 0
    
    def test_analyze_empty_text(self):
        """Test that empty text returns 422 validation error"""
        response = client.post(
            "/api/v1/analyze",
            json={"text": ""}
        )
        assert response.status_code == 422
    
    def test_analyze_whitespace_only(self):
        """Test that whitespace-only text returns 422 validation error"""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "   "}
        )
        assert response.status_code == 422
    
    def test_analyze_long_text(self):
        """Test analysis of long text (within limit)"""
        long_text = "This is a great product. " * 50  # ~150 chars
        response = client.post(
            "/api/v1/analyze",
            json={"text": long_text}
        )
        assert response.status_code == 200
    
    def test_analyze_text_too_long(self):
        """Test that text exceeding max length returns 422 error"""
        too_long = "A" * 5001  # Exceeds 5000 char limit
        response = client.post(
            "/api/v1/analyze",
            json={"text": too_long}
        )
        assert response.status_code == 422
    
    def test_analyze_missing_text_field(self):
        """Test that missing text field returns 422 error"""
        response = client.post(
            "/api/v1/analyze",
            json={}
        )
        assert response.status_code == 422


class TestBatchAnalyzeEndpoint:
    """Tests for batch analysis endpoint"""
    
    def test_batch_analyze_multiple_texts(self):
        """Test batch analysis of multiple texts"""
        response = client.post(
            "/api/v1/batch-analyze",
            json={
                "texts": [
                    "Great product!",
                    "Terrible service.",
                    "It's okay."
                ]
            }
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "total_analyzed" in data
        assert "results" in data
        assert "processing_time_ms" in data
        assert data["total_analyzed"] == 3
        assert len(data["results"]) == 3
        
        # Check each result has required fields
        for result in data["results"]:
            assert "text" in result
            assert "label" in result
            assert "score" in result
            assert "timestamp" in result
    
    def test_batch_analyze_single_text(self):
        """Test batch analysis with single text"""
        response = client.post(
            "/api/v1/batch-analyze",
            json={"texts": ["This is amazing!"]}
        )
        assert response.status_code == 200
        assert response.json()["total_analyzed"] == 1
    
    def test_batch_analyze_empty_list(self):
        """Test that empty list returns 422 error"""
        response = client.post(
            "/api/v1/batch-analyze",
            json={"texts": []}
        )
        assert response.status_code == 422
    
    def test_batch_analyze_all_empty_texts(self):
        """Test that all empty texts returns 422 error"""
        response = client.post(
            "/api/v1/batch-analyze",
            json={"texts": ["", "  ", "\n"]}
        )
        assert response.status_code == 422
    
    def test_batch_analyze_mixed_sentiments(self):
        """Test batch with mixed sentiment results"""
        response = client.post(
            "/api/v1/batch-analyze",
            json={
                "texts": [
                    "Excellent!",
                    "Awful!",
                    "Good",
                    "Bad"
                ]
            }
        )
        assert response.status_code == 200
        
        data = response.json()
        labels = [r["label"] for r in data["results"]]
        
        # Should have both positive and negative
        assert "POSITIVE" in labels
        assert "NEGATIVE" in labels
    
    def test_batch_analyze_too_many_texts(self):
        """Test that >100 texts returns 422 error"""
        too_many = ["text"] * 101
        response = client.post(
            "/api/v1/batch-analyze",
            json={"texts": too_many}
        )
        assert response.status_code == 422
    
    def test_batch_analyze_processing_time(self):
        """Test that processing time is reasonable"""
        response = client.post(
            "/api/v1/batch-analyze",
            json={"texts": ["Test"] * 10}
        )
        assert response.status_code == 200
        
        data = response.json()
        # Processing time should be positive and reasonable (< 10 seconds)
        assert data["processing_time_ms"] > 0
        assert data["processing_time_ms"] < 10000


class TestAPIDocumentation:
    """Tests for API documentation endpoints"""
    
    def test_openapi_json_available(self):
        """Test that OpenAPI JSON is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_swagger_docs_available(self):
        """Test that Swagger UI is available"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_available(self):
        """Test that ReDoc is available"""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestAPIHeaders:
    """Tests for API response headers"""
    
    def test_process_time_header(self):
        """Test that X-Process-Time-Ms header is added"""
        response = client.get("/api/v1/health")
        assert "X-Process-Time-Ms" in response.headers
        
        # Should be a valid number
        process_time = float(response.headers["X-Process-Time-Ms"])
        assert process_time >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

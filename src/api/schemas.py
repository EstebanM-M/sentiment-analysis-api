"""
Pydantic schemas for API request/response validation
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


# Request Schemas
class TextAnalysisRequest(BaseModel):
    """Request schema for single text analysis"""
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Text to analyze for sentiment",
        example="I love this product! It's amazing and works perfectly."
    )
    return_all_scores: bool = Field(
        default=False,
        description="Return scores for all labels (POSITIVE and NEGATIVE)"
    )
    
    @validator('text')
    def text_not_empty(cls, v):
        """Validate that text is not just whitespace"""
        if not v.strip():
            raise ValueError('Text cannot be empty or only whitespace')
        return v.strip()


class BatchAnalysisRequest(BaseModel):
    """Request schema for batch text analysis"""
    texts: List[str] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="List of texts to analyze (max 100)",
        example=[
            "Great product!",
            "Terrible experience.",
            "It's okay, nothing special."
        ]
    )
    return_all_scores: bool = Field(
        default=False,
        description="Return scores for all labels"
    )
    
    @validator('texts')
    def validate_texts(cls, v):
        """Validate that at least one text is non-empty"""
        valid_texts = [t for t in v if t and t.strip()]
        if not valid_texts:
            raise ValueError('At least one text must be non-empty')
        return [t.strip() if t else t for t in v]


# Response Schemas
class SentimentPrediction(BaseModel):
    """Single sentiment prediction"""
    label: str = Field(
        ...,
        description="Sentiment label (POSITIVE or NEGATIVE)"
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score (0-1)"
    )


class SentimentResult(BaseModel):
    """Result schema for single text analysis"""
    text: str = Field(..., description="Original text analyzed")
    label: str = Field(..., description="Sentiment label")
    score: float = Field(..., description="Confidence score")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Analysis timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "I love this product!",
                "label": "POSITIVE",
                "score": 0.9987,
                "timestamp": "2025-01-03T12:00:00Z"
            }
        }


class SentimentResultWithScores(BaseModel):
    """Result schema with all label scores"""
    text: str = Field(..., description="Original text analyzed")
    predictions: List[SentimentPrediction] = Field(
        ...,
        description="All sentiment predictions with scores"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Analysis timestamp"
    )


class BatchAnalysisResult(BaseModel):
    """Result schema for batch analysis"""
    total_analyzed: int = Field(..., description="Total texts analyzed")
    results: List[SentimentResult] = Field(..., description="Analysis results")
    processing_time_ms: float = Field(
        ...,
        description="Total processing time in milliseconds"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_analyzed": 3,
                "results": [
                    {
                        "text": "Great!",
                        "label": "POSITIVE",
                        "score": 0.9995,
                        "timestamp": "2025-01-03T12:00:00Z"
                    }
                ],
                "processing_time_ms": 125.5
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="API status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    model_info: Dict[str, str] = Field(..., description="Model information")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Health check timestamp"
    )


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation error",
                "detail": "Text cannot be empty",
                "timestamp": "2025-01-03T12:00:00Z"
            }
        }


class StatsResponse(BaseModel):
    """Statistics response"""
    total_analyses: int = Field(..., description="Total analyses performed")
    positive_count: int = Field(..., description="Number of positive sentiments")
    negative_count: int = Field(..., description="Number of negative sentiments")
    positive_percentage: float = Field(..., description="Percentage of positive sentiments")
    negative_percentage: float = Field(..., description="Percentage of negative sentiments")
    average_score: float = Field(..., description="Average confidence score")
    average_processing_time_ms: float = Field(..., description="Average processing time in ms")


class AnalysisHistoryItem(BaseModel):
    """Single item in analysis history"""
    id: int = Field(..., description="Analysis ID")
    text: str = Field(..., description="Analyzed text")
    label: str = Field(..., description="Sentiment label")
    score: float = Field(..., description="Confidence score")
    created_at: datetime = Field(..., description="When the analysis was performed")
    processing_time_ms: Optional[float] = Field(None, description="Processing time")
    model_name: Optional[str] = Field(None, description="Model used")
    is_batch: bool = Field(..., description="Whether this was part of a batch")
    
    class Config:
        from_attributes = True


class AnalysisHistoryResponse(BaseModel):
    """Response with analysis history"""
    total: int = Field(..., description="Total number of analyses")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    analyses: List[AnalysisHistoryItem] = Field(..., description="List of analyses")


class DateRangeStats(BaseModel):
    """Statistics for a date range"""
    dates: Dict[str, int] = Field(..., description="Count of analyses per date")
    total: int = Field(..., description="Total analyses in range")

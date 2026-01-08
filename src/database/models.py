"""
Database models for sentiment analysis
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class SentimentAnalysis(Base):
    """
    Model for storing sentiment analysis results
    """
    __tablename__ = "sentiment_analyses"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Analysis data
    text = Column(Text, nullable=False)
    label = Column(String(20), nullable=False)  # POSITIVE or NEGATIVE
    score = Column(Float, nullable=False)  # Confidence score (0-1)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processing_time_ms = Column(Float, nullable=True)  # Time taken to analyze
    
    # Optional fields
    model_name = Column(String(100), nullable=True)
    is_batch = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<SentimentAnalysis(id={self.id}, label={self.label}, score={self.score})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "text": self.text,
            "label": self.label,
            "score": self.score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "processing_time_ms": self.processing_time_ms,
            "model_name": self.model_name,
            "is_batch": self.is_batch
        }


class AnalysisStats(Base):
    """
    Model for storing aggregated statistics
    Useful for quick dashboard queries
    """
    __tablename__ = "analysis_stats"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Date for the stats (daily aggregation)
    date = Column(DateTime(timezone=True), nullable=False, index=True, unique=True)
    
    # Aggregated counts
    total_analyses = Column(Integer, default=0, nullable=False)
    positive_count = Column(Integer, default=0, nullable=False)
    negative_count = Column(Integer, default=0, nullable=False)
    
    # Aggregated metrics
    average_score = Column(Float, nullable=True)
    average_processing_time = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<AnalysisStats(date={self.date}, total={self.total_analyses})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "total_analyses": self.total_analyses,
            "positive_count": self.positive_count,
            "negative_count": self.negative_count,
            "average_score": self.average_score,
            "average_processing_time": self.average_processing_time,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

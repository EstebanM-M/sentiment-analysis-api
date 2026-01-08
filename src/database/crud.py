"""
CRUD operations for sentiment analysis database
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from database.models import SentimentAnalysis, AnalysisStats
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# SENTIMENT ANALYSIS CRUD
# ============================================================================

def create_analysis(
    db: Session,
    text: str,
    label: str,
    score: float,
    processing_time_ms: Optional[float] = None,
    model_name: Optional[str] = None,
    is_batch: bool = False
) -> SentimentAnalysis:
    """
    Create a new sentiment analysis record
    
    Args:
        db: Database session
        text: Analyzed text
        label: Sentiment label (POSITIVE/NEGATIVE)
        score: Confidence score (0-1)
        processing_time_ms: Time taken to analyze
        model_name: Name of the model used
        is_batch: Whether this was part of a batch analysis
    
    Returns:
        Created SentimentAnalysis object
    """
    try:
        analysis = SentimentAnalysis(
            text=text,
            label=label,
            score=score,
            processing_time_ms=processing_time_ms,
            model_name=model_name,
            is_batch=is_batch
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        logger.debug(f"Created analysis: {analysis.id}")
        return analysis
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating analysis: {str(e)}")
        raise


def get_analysis_by_id(db: Session, analysis_id: int) -> Optional[SentimentAnalysis]:
    """
    Get a specific analysis by ID
    """
    return db.query(SentimentAnalysis).filter(SentimentAnalysis.id == analysis_id).first()


def get_analyses(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    label: Optional[str] = None,
    min_score: Optional[float] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[SentimentAnalysis]:
    """
    Get list of analyses with optional filters
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        label: Filter by label (POSITIVE/NEGATIVE)
        min_score: Filter by minimum confidence score
        start_date: Filter by start date
        end_date: Filter by end date
    
    Returns:
        List of SentimentAnalysis objects
    """
    query = db.query(SentimentAnalysis)
    
    # Apply filters
    if label:
        query = query.filter(SentimentAnalysis.label == label)
    
    if min_score is not None:
        query = query.filter(SentimentAnalysis.score >= min_score)
    
    if start_date:
        query = query.filter(SentimentAnalysis.created_at >= start_date)
    
    if end_date:
        query = query.filter(SentimentAnalysis.created_at <= end_date)
    
    # Order by most recent first
    query = query.order_by(desc(SentimentAnalysis.created_at))
    
    # Apply pagination
    return query.offset(skip).limit(limit).all()


def get_total_analyses_count(db: Session) -> int:
    """Get total number of analyses in database"""
    return db.query(SentimentAnalysis).count()


def delete_analysis(db: Session, analysis_id: int) -> bool:
    """
    Delete an analysis by ID
    
    Returns:
        True if deleted, False if not found
    """
    try:
        analysis = get_analysis_by_id(db, analysis_id)
        if analysis:
            db.delete(analysis)
            db.commit()
            logger.debug(f"Deleted analysis: {analysis_id}")
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting analysis: {str(e)}")
        raise


# ============================================================================
# STATISTICS AND AGGREGATIONS
# ============================================================================

def get_statistics(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Get aggregated statistics for analyses
    
    Args:
        db: Database session
        start_date: Filter by start date
        end_date: Filter by end date
    
    Returns:
        Dictionary with statistics
    """
    query = db.query(SentimentAnalysis)
    
    # Apply date filters
    if start_date:
        query = query.filter(SentimentAnalysis.created_at >= start_date)
    if end_date:
        query = query.filter(SentimentAnalysis.created_at <= end_date)
    
    # Get counts by label
    total_count = query.count()
    positive_count = query.filter(SentimentAnalysis.label == "POSITIVE").count()
    negative_count = query.filter(SentimentAnalysis.label == "NEGATIVE").count()
    
    # Get average score
    avg_score = db.query(func.avg(SentimentAnalysis.score)).scalar()
    
    # Get average processing time
    avg_processing_time = db.query(
        func.avg(SentimentAnalysis.processing_time_ms)
    ).filter(
        SentimentAnalysis.processing_time_ms.isnot(None)
    ).scalar()
    
    return {
        "total_analyses": total_count,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "positive_percentage": (positive_count / total_count * 100) if total_count > 0 else 0,
        "negative_percentage": (negative_count / total_count * 100) if total_count > 0 else 0,
        "average_score": float(avg_score) if avg_score else 0.0,
        "average_processing_time_ms": float(avg_processing_time) if avg_processing_time else 0.0
    }


def get_recent_analyses(db: Session, limit: int = 10) -> List[SentimentAnalysis]:
    """
    Get most recent analyses
    
    Args:
        db: Database session
        limit: Number of analyses to return
    
    Returns:
        List of most recent SentimentAnalysis objects
    """
    return db.query(SentimentAnalysis).order_by(
        desc(SentimentAnalysis.created_at)
    ).limit(limit).all()


def get_analyses_by_date_range(
    db: Session,
    days: int = 7
) -> Dict[str, int]:
    """
    Get count of analyses for the last N days, grouped by day
    
    Args:
        db: Database session
        days: Number of days to look back
    
    Returns:
        Dictionary with date as key and count as value
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Query to get analyses grouped by date
    results = db.query(
        func.date(SentimentAnalysis.created_at).label('date'),
        func.count(SentimentAnalysis.id).label('count')
    ).filter(
        SentimentAnalysis.created_at >= start_date
    ).group_by(
        func.date(SentimentAnalysis.created_at)
    ).all()
    
    # Convert to dictionary
    data = {str(result.date): result.count for result in results}
    
    # Fill in missing dates with 0
    current_date = start_date.date()
    while current_date <= end_date.date():
        date_str = str(current_date)
        if date_str not in data:
            data[date_str] = 0
        current_date += timedelta(days=1)
    
    return dict(sorted(data.items()))


def search_analyses(
    db: Session,
    search_term: str,
    limit: int = 50
) -> List[SentimentAnalysis]:
    """
    Search analyses by text content
    
    Args:
        db: Database session
        search_term: Text to search for
        limit: Maximum number of results
    
    Returns:
        List of matching SentimentAnalysis objects
    """
    return db.query(SentimentAnalysis).filter(
        SentimentAnalysis.text.ilike(f"%{search_term}%")
    ).order_by(
        desc(SentimentAnalysis.created_at)
    ).limit(limit).all()


# ============================================================================
# DAILY STATS (for efficient dashboard queries)
# ============================================================================

def update_daily_stats(db: Session, date: datetime):
    """
    Update or create daily statistics for a given date
    This can be run as a background job
    
    Args:
        db: Database session
        date: Date to calculate stats for
    """
    try:
        # Get all analyses for the date
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        analyses = db.query(SentimentAnalysis).filter(
            SentimentAnalysis.created_at >= start_of_day,
            SentimentAnalysis.created_at < end_of_day
        ).all()
        
        if not analyses:
            return
        
        # Calculate statistics
        total = len(analyses)
        positive = sum(1 for a in analyses if a.label == "POSITIVE")
        negative = total - positive
        avg_score = sum(a.score for a in analyses) / total
        
        # Calculate average processing time (only for non-null values)
        processing_times = [a.processing_time_ms for a in analyses if a.processing_time_ms is not None]
        avg_processing = sum(processing_times) / len(processing_times) if processing_times else None
        
        # Check if stats already exist for this date
        stats = db.query(AnalysisStats).filter(
            func.date(AnalysisStats.date) == date.date()
        ).first()
        
        if stats:
            # Update existing
            stats.total_analyses = total
            stats.positive_count = positive
            stats.negative_count = negative
            stats.average_score = avg_score
            stats.average_processing_time = avg_processing
            stats.updated_at = datetime.utcnow()
        else:
            # Create new
            stats = AnalysisStats(
                date=start_of_day,
                total_analyses=total,
                positive_count=positive,
                negative_count=negative,
                average_score=avg_score,
                average_processing_time=avg_processing
            )
            db.add(stats)
        
        db.commit()
        logger.debug(f"Updated stats for {date.date()}")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating daily stats: {str(e)}")
        raise

"""
Sentiment analysis API routes
"""

from fastapi import APIRouter, HTTPException, Request, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
import time
import logging

from api.schemas import (
    TextAnalysisRequest,
    BatchAnalysisRequest,
    SentimentResult,
    SentimentResultWithScores,
    BatchAnalysisResult,
    HealthResponse,
    ErrorResponse,
    StatsResponse,
    AnalysisHistoryResponse,
    AnalysisHistoryItem,
    DateRangeStats
)
from database.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/analyze",
    response_model=SentimentResult | SentimentResultWithScores,
    summary="Analyze sentiment of a single text",
    description="""
    Analyze the sentiment of a single text input.
    
    Returns the sentiment label (POSITIVE/NEGATIVE) and confidence score.
    Optionally, return scores for all labels by setting `return_all_scores=true`.
    """,
    responses={
        200: {
            "description": "Successful analysis",
            "model": SentimentResult
        },
        400: {
            "description": "Invalid input",
            "model": ErrorResponse
        },
        500: {
            "description": "Server error",
            "model": ErrorResponse
        }
    }
)
async def analyze_sentiment(
    request: TextAnalysisRequest,
    req: Request,
    db: Session = Depends(get_db)
):
    """
    Analyze sentiment of a single text
    
    - **text**: Text to analyze (1-5000 characters)
    - **return_all_scores**: Return scores for all labels (optional, default: false)
    """
    try:
        analyzer = req.app.state.analyzer
        
        # Start timing
        start_time = time.time()
        
        # Perform analysis
        result = analyzer.analyze(
            text=request.text,
            return_all_scores=request.return_all_scores
        )
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Save to database
        try:
            from database import crud
            crud.create_analysis(
                db=db,
                text=result["text"],
                label=result["label"] if not request.return_all_scores else result["predictions"][0]["label"],
                score=result["score"] if not request.return_all_scores else result["predictions"][0]["score"],
                processing_time_ms=processing_time,
                model_name=analyzer.model_name,
                is_batch=False
            )
        except Exception as db_error:
            logger.warning(f"Failed to save to database: {str(db_error)}")
            # Continue anyway - analysis succeeded even if DB save failed
        
        # Format response
        if request.return_all_scores:
            return SentimentResultWithScores(
                text=result["text"],
                predictions=result["predictions"],
                timestamp=datetime.utcnow()
            )
        else:
            return SentimentResult(
                text=result["text"],
                label=result["label"],
                score=result["score"],
                timestamp=datetime.utcnow()
            )
            
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing request")


@router.post(
    "/batch-analyze",
    response_model=BatchAnalysisResult,
    summary="Analyze sentiment of multiple texts",
    description="""
    Analyze the sentiment of multiple texts in a single request.
    
    Supports up to 100 texts per request for efficient batch processing.
    """,
    responses={
        200: {
            "description": "Successful batch analysis",
            "model": BatchAnalysisResult
        },
        400: {
            "description": "Invalid input",
            "model": ErrorResponse
        },
        500: {
            "description": "Server error",
            "model": ErrorResponse
        }
    }
)
async def batch_analyze_sentiment(
    request: BatchAnalysisRequest,
    req: Request,
    db: Session = Depends(get_db)
):
    """
    Analyze sentiment of multiple texts
    
    - **texts**: List of texts to analyze (1-100 texts)
    - **return_all_scores**: Return scores for all labels (optional, default: false)
    """
    try:
        analyzer = req.app.state.analyzer
        
        # Start timing
        start_time = time.time()
        
        # Perform batch analysis
        results = analyzer.analyze_batch(
            texts=request.texts,
            batch_size=8,
            return_all_scores=request.return_all_scores
        )
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        avg_time_per_text = processing_time / len(results) if results else 0
        
        # Save to database
        try:
            from database import crud
            for result in results:
                if request.return_all_scores:
                    top_pred = max(result["predictions"], key=lambda x: x["score"])
                    label = top_pred["label"]
                    score = top_pred["score"]
                else:
                    label = result["label"]
                    score = result["score"]
                
                crud.create_analysis(
                    db=db,
                    text=result["text"],
                    label=label,
                    score=score,
                    processing_time_ms=avg_time_per_text,
                    model_name=analyzer.model_name,
                    is_batch=True
                )
        except Exception as db_error:
            logger.warning(f"Failed to save batch to database: {str(db_error)}")
            # Continue anyway
        
        # Format results
        formatted_results = []
        for result in results:
            if request.return_all_scores:
                # For now, just use the top prediction
                top_pred = max(result["predictions"], key=lambda x: x["score"])
                formatted_results.append(
                    SentimentResult(
                        text=result["text"],
                        label=top_pred["label"],
                        score=top_pred["score"],
                        timestamp=datetime.utcnow()
                    )
                )
            else:
                formatted_results.append(
                    SentimentResult(
                        text=result["text"],
                        label=result["label"],
                        score=result["score"],
                        timestamp=datetime.utcnow()
                    )
                )
        
        return BatchAnalysisResult(
            total_analyzed=len(formatted_results),
            results=formatted_results,
            processing_time_ms=round(processing_time, 2)
        )
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing batch request")


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check endpoint",
    description="Check the health status of the API and model availability"
)
async def health_check(req: Request):
    """
    Health check endpoint
    
    Returns the status of the API and model information
    """
    try:
        analyzer = req.app.state.analyzer
        model_info = analyzer.get_model_info()
        
        return HealthResponse(
            status="healthy",
            model_loaded=True,
            model_info=model_info,
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            model_loaded=False,
            model_info={},
            timestamp=datetime.utcnow()
        )


@router.get(
    "/model-info",
    summary="Get model information",
    description="Get detailed information about the loaded sentiment analysis model"
)
async def get_model_info(req: Request):
    """
    Get model information
    
    Returns detailed information about the sentiment analysis model
    """
    try:
        analyzer = req.app.state.analyzer
        info = analyzer.get_model_info()
        
        return {
            "model": info,
            "capabilities": {
                "single_analysis": True,
                "batch_analysis": True,
                "max_batch_size": 100,
                "max_text_length": 512
            },
            "performance": {
                "model_accuracy": "~95% on SST-2 benchmark",
                "inference_device": info["device"]
            }
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving model information")


@router.get(
    "/history",
    response_model=AnalysisHistoryResponse,
    summary="Get analysis history",
    description="Retrieve history of sentiment analyses with pagination and filtering"
)
async def get_history(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    label: Optional[str] = Query(None, description="Filter by label (POSITIVE/NEGATIVE)"),
    min_score: Optional[float] = Query(None, ge=0, le=1, description="Filter by minimum score")
):
    """
    Get paginated history of analyses
    
    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page (max 100)
    - **label**: Filter by sentiment label (optional)
    - **min_score**: Filter by minimum confidence score (optional)
    """
    try:
        from database import crud
        
        # Calculate skip
        skip = (page - 1) * page_size
        
        # Get analyses
        analyses = crud.get_analyses(
            db=db,
            skip=skip,
            limit=page_size,
            label=label,
            min_score=min_score
        )
        
        # Get total count
        total = crud.get_total_analyses_count(db)
        
        # Convert to Pydantic models
        analysis_items = [
            AnalysisHistoryItem.model_validate(analysis)
            for analysis in analyses
        ]
        
        return AnalysisHistoryResponse(
            total=total,
            page=page,
            page_size=page_size,
            analyses=analysis_items
        )
        
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving history")


@router.get(
    "/stats",
    response_model=StatsResponse,
    summary="Get statistics",
    description="Get aggregated statistics about sentiment analyses"
)
async def get_stats(
    db: Session = Depends(get_db),
    days: Optional[int] = Query(None, ge=1, le=365, description="Limit stats to last N days")
):
    """
    Get aggregated statistics
    
    - **days**: Limit to last N days (optional)
    """
    try:
        from database import crud
        from datetime import datetime, timedelta
        
        start_date = None
        if days:
            start_date = datetime.utcnow() - timedelta(days=days)
        
        stats = crud.get_statistics(db=db, start_date=start_date)
        
        return StatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")


@router.get(
    "/stats/timeline",
    response_model=DateRangeStats,
    summary="Get timeline statistics",
    description="Get count of analyses per day for a date range"
)
async def get_timeline_stats(
    db: Session = Depends(get_db),
    days: int = Query(7, ge=1, le=90, description="Number of days to include")
):
    """
    Get timeline of analyses
    
    Returns count of analyses for each day in the specified range
    
    - **days**: Number of days to look back (default: 7, max: 90)
    """
    try:
        from database import crud
        
        data = crud.get_analyses_by_date_range(db=db, days=days)
        
        return DateRangeStats(
            dates=data,
            total=sum(data.values())
        )
        
    except Exception as e:
        logger.error(f"Error getting timeline stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving timeline")


@router.get(
    "/search",
    response_model=List[AnalysisHistoryItem],
    summary="Search analyses",
    description="Search through analysis history by text content"
)
async def search_analyses(
    db: Session = Depends(get_db),
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results")
):
    """
    Search analyses by text content
    
    - **q**: Search query (required)
    - **limit**: Maximum number of results (default: 50, max: 100)
    """
    try:
        from database import crud
        
        analyses = crud.search_analyses(db=db, search_term=q, limit=limit)
        
        return [
            AnalysisHistoryItem.model_validate(analysis)
            for analysis in analyses
        ]
        
    except Exception as e:
        logger.error(f"Error searching analyses: {str(e)}")
        raise HTTPException(status_code=500, detail="Error performing search")

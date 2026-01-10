"""
Main FastAPI application
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from api.config import settings
from models.sentiment_model import get_analyzer

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup: Load the model and initialize database
    logger.info("Starting up API...")
    
    # Initialize database
    try:
        from database.database import init_db
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        # Continue anyway - API can work without database
    
    # Load sentiment analysis model
    logger.info("Loading sentiment analysis model...")
    try:
        # Import memory optimization
        from utils.memory_optimization import optimize_memory
        
        analyzer = get_analyzer(
            model_name=settings.MODEL_NAME,
            cache_dir=settings.MODEL_CACHE_DIR
        )
        logger.info(f"Model loaded successfully: {analyzer.model_name}")
        logger.info(f"Using device: {analyzer.device}")
        
        # Optimize memory after loading model
        optimize_memory()
        logger.info("Memory optimization applied")
        
        # Store analyzer in app state
        app.state.analyzer = analyzer
        
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise
    
    logger.info("API startup complete!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down API...")
    try:
        from database.database import close_db
        close_db()
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# Add request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    response.headers["X-Process-Time-Ms"] = str(round(process_time, 2))
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Sentiment Analysis API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


# Import and include routers
from api.routes import sentiment

app.include_router(
    sentiment.router,
    prefix="/api/v1",
    tags=["Sentiment Analysis"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )

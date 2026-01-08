"""
Database configuration and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import logging

from database.models import Base
from api.config import settings

logger = logging.getLogger(__name__)

# Create engine
# For SQLite (development/testing)
if settings.DATABASE_URL and settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DB_ECHO
    )
# For PostgreSQL (production)
else:
    engine = create_engine(
        settings.DATABASE_URL or "sqlite:///./sentiment_analysis.db",
        pool_pre_ping=True,  # Verify connections before using
        echo=settings.DB_ECHO
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initialize database - create all tables
    Call this on application startup
    """
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database session
    Use with FastAPI Depends
    
    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def close_db():
    """
    Close database connections
    Call this on application shutdown
    """
    try:
        logger.info("Closing database connections...")
        engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {str(e)}")

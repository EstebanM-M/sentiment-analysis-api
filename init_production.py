#!/usr/bin/env python
"""
Production initialization script
Run this after deployment to ensure database is set up
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def init_production():
    """Initialize production environment"""
    print("🚀 Initializing production environment...")
    
    try:
        # Import after path is set
        from database.database import init_db, engine
        from database.models import Base
        from api.config import settings
        
        print(f"📊 Database URL: {settings.DATABASE_URL[:20]}...")
        print("🔧 Creating database tables...")
        
        # Initialize database
        init_db()
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"✅ Created {len(tables)} tables: {', '.join(tables)}")
        print("🎉 Production initialization complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during initialization: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = init_production()
    sys.exit(0 if success else 1)

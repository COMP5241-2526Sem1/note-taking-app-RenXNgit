# Test Database Connection
# This script helps verify that the database configuration works correctly

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.models.user import db
    from src.models.note import Note
    from src.main import app
    
    print("🔍 Testing database configuration...")
    
    # Check environment configuration
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL:
        print(f"✅ DATABASE_URL found: {DATABASE_URL[:30]}...")
        print("📡 Using PostgreSQL configuration")
    else:
        print("⚠️  No DATABASE_URL found, using SQLite fallback")
    
    # Test database connection
    with app.app_context():
        try:
            # Try to create tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Test basic operations
            test_note = Note(title="Test Note", content="This is a test note")
            db.session.add(test_note)
            db.session.commit()
            print("✅ Test note created successfully")
            
            # Verify note exists
            notes = Note.query.all()
            print(f"✅ Found {len(notes)} notes in database")
            
            # Clean up test note
            db.session.delete(test_note)
            db.session.commit()
            print("✅ Test note cleaned up")
            
            print("\n🎉 Database configuration test completed successfully!")
            print("\nNext steps:")
            print("1. Set up your Supabase database")
            print("2. Copy .env.example to .env and update DATABASE_URL")
            print("3. Run this test again to verify cloud database connection")
            print("4. Deploy to Vercel with environment variables configured")
            
        except Exception as e:
            print(f"❌ Database operation failed: {e}")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have installed all dependencies: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
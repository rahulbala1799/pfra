#!/usr/bin/env python3
"""
Simple script to create the database with the new schema
"""

import sys
import os

# Add the current directory to Python path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_database():
    """Create the database with all tables"""
    
    print("🔧 Creating Database with New Schema")
    print("=" * 40)
    
    try:
        from app import app, db
        
        with app.app_context():
            # Drop all tables first
            db.drop_all()
            print("✅ Dropped existing tables")
            
            # Create all tables
            db.create_all()
            print("✅ Created all tables")
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Created tables: {tables}")
            
            # Check monthly_transaction table specifically
            if 'monthly_transaction' in tables:
                columns = [col['name'] for col in inspector.get_columns('monthly_transaction')]
                print(f"📋 monthly_transaction columns: {columns}")
                
                if 'source_account_id' in columns:
                    print("✅ source_account_id column exists!")
                else:
                    print("❌ source_account_id column missing!")
                    return False
            else:
                print("❌ monthly_transaction table not found!")
                return False
        
        print("\n🎉 Database created successfully with new schema!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_database()
    if success:
        print("\n✅ Ready to test debt payment tracking!")
    else:
        print("\n❌ Database creation failed.") 
#!/usr/bin/env python3
"""
Migration script to add debt payment tracking functionality
Adds source_account_id column to monthly_transaction table
"""

import sys
import os
import sqlite3

# Add the current directory to Python path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def migrate_database():
    """Add source_account_id column to monthly_transaction table"""
    
    print("🔄 Migrating Database for Debt Payment Tracking")
    print("=" * 50)
    
    try:
        # Get the database file path
        db_path = 'personal_finance.db'
        
        # Connect directly to SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(monthly_transaction)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'source_account_id' in columns:
            print("✅ source_account_id column already exists!")
            conn.close()
            return True
        
        print("📋 Current columns:", columns)
        
        # Add the new column
        print("\n🔧 Adding source_account_id column...")
        cursor.execute("""
            ALTER TABLE monthly_transaction 
            ADD COLUMN source_account_id INTEGER 
            REFERENCES bank_account(id)
        """)
        
        conn.commit()
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(monthly_transaction)")
        new_columns = [column[1] for column in cursor.fetchall()]
        
        if 'source_account_id' in new_columns:
            print("✅ Successfully added source_account_id column!")
            print("📋 New columns:", new_columns)
        else:
            print("❌ Failed to add source_account_id column!")
            return False
        
        conn.close()
        
        print("\n🎯 Migration completed successfully!")
        print("   • source_account_id column added to monthly_transaction table")
        print("   • Ready for debt payment tracking functionality")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = migrate_database()
    if success:
        print("\n🎉 Database migration successful!")
        print("You can now use debt payment tracking features.")
    else:
        print("\n💔 Database migration failed.")
        print("Please check the error and try again.") 
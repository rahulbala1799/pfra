#!/usr/bin/env python3
"""
Script to populate the personal finance app with initial bank accounts
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, BankAccount

def create_accounts():
    """Create all the bank accounts"""
    
    accounts_data = [
        # Checking Accounts
        {"name": "Ann", "account_type": "checking", "bank_name": "Ann's Bank"},
        {"name": "Rahul", "account_type": "checking", "bank_name": "Rahul's Bank"},
        
        # Savings Accounts
        {"name": "RDF", "account_type": "savings", "bank_name": "RDF Bank"},
        
        # Loan Accounts
        {"name": "Wedding Loan", "account_type": "loan", "bank_name": "Wedding Loan Provider"},
        {"name": "Xerox Loan", "account_type": "loan", "bank_name": "Xerox Loan Provider"},
        {"name": "Pita Loan", "account_type": "loan", "bank_name": "Pita Loan Provider"},
        
        # Credit Cards
        {"name": "Platinum", "account_type": "credit", "bank_name": "Platinum Card Bank"},
        {"name": "Click", "account_type": "credit", "bank_name": "Click Card Bank"},
        {"name": "Revolut", "account_type": "credit", "bank_name": "Revolut"},
    ]
    
    print("Creating bank accounts...")
    print("=" * 50)
    
    with app.app_context():
        # Check if accounts already exist to avoid duplicates
        existing_accounts = BankAccount.query.all()
        existing_names = [acc.name for acc in existing_accounts]
        
        created_count = 0
        skipped_count = 0
        
        for account_data in accounts_data:
            if account_data["name"] in existing_names:
                print(f"⏭️  SKIPPED: {account_data['name']} ({account_data['account_type']}) - already exists")
                skipped_count += 1
                continue
            
            # Create new account
            account = BankAccount(
                name=account_data["name"],
                account_type=account_data["account_type"],
                bank_name=account_data["bank_name"],
                is_active=True,
                created_date=datetime.utcnow()
            )
            
            db.session.add(account)
            print(f"✅ CREATED: {account_data['name']} ({account_data['account_type']})")
            created_count += 1
        
        # Commit all changes
        try:
            db.session.commit()
            print("=" * 50)
            print(f"✅ Successfully created {created_count} new accounts")
            if skipped_count > 0:
                print(f"⏭️  Skipped {skipped_count} existing accounts")
            print("=" * 50)
            
            # Display all accounts
            print("\n📋 ALL ACCOUNTS IN DATABASE:")
            print("-" * 30)
            all_accounts = BankAccount.query.filter_by(is_active=True).all()
            
            # Group by account type
            account_types = {}
            for acc in all_accounts:
                if acc.account_type not in account_types:
                    account_types[acc.account_type] = []
                account_types[acc.account_type].append(acc)
            
            for acc_type in ['checking', 'savings', 'loan', 'credit']:
                if acc_type in account_types:
                    print(f"\n{acc_type.upper()} ACCOUNTS:")
                    for acc in account_types[acc_type]:
                        print(f"  • {acc.name}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ ERROR: Failed to create accounts - {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    print("🏦 Personal Finance App - Account Population Script")
    print("=" * 60)
    
    success = create_accounts()
    
    if success:
        print("\n🎉 Account population completed successfully!")
        print("You can now start using your personal finance app with these accounts.")
    else:
        print("\n❌ Account population failed. Please check the errors above.")
        sys.exit(1) 
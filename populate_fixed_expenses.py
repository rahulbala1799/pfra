#!/usr/bin/env python3
"""
Script to populate the personal finance app with fixed expenses
"""

import sys
import os
from datetime import datetime, date

# Add the current directory to Python path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, FixedExpense

def create_fixed_expenses():
    """Create all the fixed expenses"""
    
    fixed_expenses_data = [
        {"name": "Rent", "amount": 975.0, "category": "Housing", "description": "Monthly rent payment"},
        {"name": "Wedding Loan", "amount": 477.0, "category": "Debt Payments", "description": "Wedding loan monthly payment"},
        {"name": "Xerox Loan", "amount": 98.0, "category": "Debt Payments", "description": "Xerox loan monthly payment"},
        {"name": "Pitaworks Loan", "amount": 40.0, "category": "Debt Payments", "description": "Pitaworks loan monthly payment"},
        {"name": "Income Protection Insurance", "amount": 127.0, "category": "Insurance", "description": "Income protection insurance premium"},
        {"name": "Arun Loan", "amount": 120.0, "category": "Debt Payments", "description": "Arun loan monthly payment"},
        {"name": "Car Insurance", "amount": 120.0, "category": "Insurance", "description": "Car insurance premium"},
        {"name": "Mobile Phone", "amount": 80.0, "category": "Utilities", "description": "Mobile phone monthly bill"},
        {"name": "Internet", "amount": 45.0, "category": "Utilities", "description": "Internet monthly subscription"}
    ]
    
    print("🏦 Populating Fixed Expenses Database")
    print("=" * 50)
    
    try:
        # Check for existing expenses and avoid duplicates
        existing_expenses = {expense.name for expense in FixedExpense.query.all()}
        
        total_amount = 0
        created_count = 0
        skipped_count = 0
        
        for expense_data in fixed_expenses_data:
            if expense_data["name"] in existing_expenses:
                print(f"⏭️  Skipped: {expense_data['name']} (already exists)")
                skipped_count += 1
                continue
            
            # Create fixed expense
            expense = FixedExpense(
                name=expense_data["name"],
                description=expense_data["description"],
                amount=expense_data["amount"],
                frequency="monthly",
                category=expense_data["category"],
                start_date=date.today(),  # Start from today
                is_active=True
            )
            
            db.session.add(expense)
            total_amount += expense_data["amount"]
            created_count += 1
            
            print(f"✅ Created: {expense_data['name']} - €{expense_data['amount']:.2f} ({expense_data['category']})")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "=" * 50)
        print(f"🎉 Successfully created {created_count} fixed expenses!")
        print(f"⏭️  Skipped {skipped_count} existing expenses")
        print(f"💰 Total monthly fixed expenses: €{total_amount:.2f}")
        
        # Show breakdown by category
        print("\n📊 Breakdown by Category:")
        category_totals = {}
        for expense_data in fixed_expenses_data:
            category = expense_data["category"]
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += expense_data["amount"]
        
        for category, amount in sorted(category_totals.items()):
            print(f"   {category}: €{amount:.2f}")
        
        # Verify database contents
        print("\n🔍 Database Verification:")
        all_expenses = FixedExpense.query.filter_by(is_active=True).all()
        print(f"✅ Total active fixed expenses in database: {len(all_expenses)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating fixed expenses: {str(e)}")
        db.session.rollback()
        return False

if __name__ == '__main__':
    with app.app_context():
        create_fixed_expenses() 
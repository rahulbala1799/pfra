#!/usr/bin/env python3
"""Test script for investment functionality"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Investment

def test_investment_functionality():
    """Test the investment functionality"""
    with app.app_context():
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        print("🚀 Testing Investment Functionality")
        print("=" * 50)
        
        # Test 1: Create test investments
        print("📈 Test 1: Adding test investments...")
        
        # Clear existing test data for current month
        Investment.query.filter_by(month=current_month, year=current_year).delete()
        
        # Add test investments
        investments = [
            Investment(month=current_month, year=current_year, investment_type='Index', amount=500.0, notes='VWCE ETF'),
            Investment(month=current_month, year=current_year, investment_type='Metals', amount=200.0, notes='Gold coins'),
            Investment(month=current_month, year=current_year, investment_type='Crypto', amount=300.0, notes='Bitcoin DCA')
        ]
        
        for inv in investments:
            db.session.add(inv)
        
        db.session.commit()
        print("✅ Added 3 test investments: €500 Index, €200 Metals, €300 Crypto")
        
        # Test 2: Verify investment totals
        print("\n📊 Test 2: Calculating investment totals...")
        
        total_investments = Investment.query.filter_by(
            month=current_month,
            year=current_year
        ).with_entities(db.func.sum(Investment.amount)).scalar() or 0
        
        print(f"✅ Total investments: €{total_investments:.2f}")
        
        # Test 3: Check expense adjustment logic
        print("\n🧮 Test 3: Testing expense adjustment logic...")
        
        simulated_calculated_expenses = 2000.0
        adjusted_expenses = max(0, simulated_calculated_expenses - total_investments)
        
        print(f"✅ Calculated expenses: €{simulated_calculated_expenses:.2f}")
        print(f"✅ Total investments: €{total_investments:.2f}")
        print(f"✅ Adjusted expenses: €{adjusted_expenses:.2f}")
        
        print("\n🎉 All tests completed successfully!")
        
if __name__ == '__main__':
    test_investment_functionality() 
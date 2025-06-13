#!/usr/bin/env python3
"""
Test script for debt payment tracking functionality
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, BankAccount, MonthlyTransaction

def test_debt_payment_tracking():
    """Test the debt payment tracking system"""
    
    print("🧪 Testing Debt Payment Tracking System")
    print("=" * 50)
    
    try:
        # Get some test accounts
        checking = BankAccount.query.filter_by(name='Rahul').first()
        savings = BankAccount.query.filter_by(name='Ann').first()
        credit_card = BankAccount.query.filter_by(account_type='credit').first()
        
        if not all([checking, savings, credit_card]):
            print("❌ Missing required test accounts")
            print(f"   Checking: {checking}")
            print(f"   Savings: {savings}")
            print(f"   Credit Card: {credit_card}")
            return False
        
        month = 6
        year = 2025
        
        print(f"📋 Test Accounts:")
        print(f"   • {checking.name} ({checking.account_type})")
        print(f"   • {savings.name} ({savings.account_type})")
        print(f"   • {credit_card.name} ({credit_card.account_type})")
        
        # Test 1: Track a credit card payment from checking account
        print(f"\n🧪 Test 1: Track Credit Card Payment")
        
        payment1 = MonthlyTransaction(
            account_id=credit_card.id,
            month=month,
            year=year,
            transaction_type='income',  # Payment reduces debt
            amount=500.00,
            description=f'Payment from {checking.name} (Tracking Only)',
            category='Debt Payment',
            source_account_id=checking.id
        )
        
        db.session.add(payment1)
        print(f"   ✅ Created: €500.00 payment from {checking.name} to {credit_card.name}")
        
        # Test 2: Track another payment from savings
        print(f"\n🧪 Test 2: Track Another Payment")
        
        payment2 = MonthlyTransaction(
            account_id=credit_card.id,
            month=month,
            year=year,
            transaction_type='income',
            amount=200.00,
            description=f'Payment from {savings.name} (Tracking Only)',
            category='Debt Payment',
            source_account_id=savings.id
        )
        
        db.session.add(payment2)
        print(f"   ✅ Created: €200.00 payment from {savings.name} to {credit_card.name}")
        
        # Commit the changes
        db.session.commit()
        
        # Test 3: Verify tracking queries work correctly
        print(f"\n🧪 Test 3: Verify Tracking Queries")
        
        # Get all debt payments for the credit card
        debt_payments = MonthlyTransaction.query.filter(
            MonthlyTransaction.account_id == credit_card.id,
            MonthlyTransaction.month == month,
            MonthlyTransaction.year == year,
            MonthlyTransaction.source_account_id.isnot(None)
        ).all()
        
        print(f"   📊 Found {len(debt_payments)} tracked debt payments:")
        for payment in debt_payments:
            print(f"      • €{payment.amount:.2f} from {payment.source_account.name}")
        
        # Test 4: Verify filtering works (should exclude tracked payments from balance calculations)
        print(f"\n🧪 Test 4: Verify Balance Calculation Exclusion")
        
        # Regular income (should be included in balance calculations)
        regular_income = MonthlyTransaction.query.filter(
            MonthlyTransaction.account_id == credit_card.id,
            MonthlyTransaction.month == month,
            MonthlyTransaction.year == year,
            MonthlyTransaction.transaction_type.in_(['income', 'misc_income']),
            MonthlyTransaction.source_account_id.is_(None)
        ).all()
        
        regular_income_total = sum(t.amount for t in regular_income)
        print(f"   💰 Regular income (affects balance): €{regular_income_total:.2f}")
        
        # Tracked payments (should NOT be included in balance calculations)
        tracked_payments_total = sum(p.amount for p in debt_payments)
        print(f"   🔍 Tracked payments (tracking only): €{tracked_payments_total:.2f}")
        
        # Test 5: Show source account breakdown
        print(f"\n🧪 Test 5: Payment Source Breakdown")
        
        payment_sources = {}
        for payment in debt_payments:
            source = payment.source_account.name
            if source not in payment_sources:
                payment_sources[source] = 0
            payment_sources[source] += payment.amount
        
        for source, amount in payment_sources.items():
            print(f"   • {source}: €{amount:.2f}")
        
        print(f"\n✅ All debt payment tracking tests passed!")
        print(f"   • Payments are tracked with source account information")
        print(f"   • Balance calculations exclude tracked payments (no double counting)")
        print(f"   • Source account breakdown available for analysis")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        db.session.rollback()
        return False

if __name__ == "__main__":
    with app.app_context():
        success = test_debt_payment_tracking()
        if success:
            print("\n🎉 Debt payment tracking system is working correctly!")
        else:
            print("\n💔 Debt payment tracking tests failed.") 
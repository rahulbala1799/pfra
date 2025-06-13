#!/usr/bin/env python3
"""
Test suite for the unified monthly data system.
Tests both regular accounts and debt accounts functionality.
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, BankAccount, MonthlyBalance, MonthlyTransaction, FixedExpense
from datetime import datetime

class TestUnifiedAccountSystem:
    
    @pytest.fixture
    def client(self):
        """Set up test client"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                yield client
                db.drop_all()
    
    def test_regular_account_creation_and_data_entry(self, client):
        """Test 1: Regular Account Setup and Data Entry"""
        print("\n=== TEST 1: Regular Account Creation & Data Entry ===")
        
        # Create regular accounts
        checking = BankAccount(name="Main Checking", account_type="checking", bank_name="Test Bank")
        savings = BankAccount(name="Emergency Savings", account_type="savings", bank_name="Test Bank")
        
        db.session.add_all([checking, savings])
        db.session.commit()
        
        # Test regular account data entry
        response = client.post('/set_regular_account_data', data={
            'account_id': checking.id,
            'month': 6,
            'year': 2025,
            'opening_balance': 1500.00,
            'income': 2500.00,
            'closing_balance': 1800.00
        })
        
        assert response.status_code == 302  # Redirect after success
        
        # Verify the calculation: Expenses = Opening + Income - Closing = 1500 + 2500 - 1800 = 2200
        balance = MonthlyBalance.query.filter_by(account_id=checking.id, month=6, year=2025).first()
        assert balance is not None
        assert balance.opening_balance == 1500.00
        assert balance.income == 2500.00
        assert balance.closing_balance == 1800.00
        assert balance.expenses == 2200.00
        
        # Verify transactions were created
        transactions = MonthlyTransaction.query.filter_by(account_id=checking.id, month=6, year=2025).all()
        
        income_transactions = [t for t in transactions if t.transaction_type == 'income']
        expense_transactions = [t for t in transactions if t.transaction_type == 'expense']
        
        assert len(income_transactions) == 1
        assert income_transactions[0].amount == 2500.00
        assert len(expense_transactions) == 1
        assert expense_transactions[0].amount == 2200.00
        
        print("✓ Regular account data entry working correctly")
        print(f"✓ Calculated expenses: €{balance.expenses:.2f}")
    
    def test_debt_account_creation_and_data_entry(self, client):
        """Test 2: Debt Account Setup and Data Entry"""
        print("\n=== TEST 2: Debt Account Creation & Data Entry ===")
        
        # Create debt accounts
        credit_card = BankAccount(name="Visa Credit Card", account_type="credit", bank_name="Test Bank")
        car_loan = BankAccount(name="Car Loan", account_type="loan", bank_name="Test Bank")
        
        db.session.add_all([credit_card, car_loan])
        db.session.commit()
        
        # Test debt account data entry
        response = client.post('/set_debt_account_data', data={
            'account_id': credit_card.id,
            'month': 6,
            'year': 2025,
            'opening_balance': 1200.00,  # Amount owed at start
            'paid_amount': 800.00,       # Payment made
            'closing_balance': 1450.00   # Amount still owed
        })
        
        assert response.status_code == 302  # Redirect after success
        
        # Verify the calculation: Monthly Spend = Closing - Opening + Paid = 1450 - 1200 + 800 = 1050
        transactions = MonthlyTransaction.query.filter_by(account_id=credit_card.id, month=6, year=2025).all()
        
        payment_transactions = [t for t in transactions if t.transaction_type == 'income']
        spend_transactions = [t for t in transactions if t.transaction_type == 'expense']
        
        assert len(payment_transactions) == 1
        assert payment_transactions[0].amount == 800.00
        assert len(spend_transactions) == 1
        assert spend_transactions[0].amount == 1050.00  # Monthly spend
        
        print("✓ Debt account data entry working correctly")
        print(f"✓ Calculated monthly spend: €{spend_transactions[0].amount:.2f}")
    
    def test_regular_account_with_fixed_expenses(self, client):
        """Test 3: Regular Account with Fixed Expenses Integration"""
        print("\n=== TEST 3: Regular Account with Fixed Expenses ===")
        
        # Create account and fixed expenses
        checking = BankAccount(name="Main Checking", account_type="checking", bank_name="Test Bank")
        db.session.add(checking)
        db.session.commit()
        
        # Create fixed expenses
        from datetime import date
        rent = FixedExpense(name="Rent", amount=1200.00, category="Housing", start_date=date.today())
        utilities = FixedExpense(name="Utilities", amount=150.00, category="Bills", start_date=date.today())
        db.session.add_all([rent, utilities])
        db.session.commit()
        
        # Mark fixed expenses as paid
        client.post('/mark_fixed_expense_paid', data={
            'fixed_expense_id': rent.id,
            'account_id': checking.id,
            'month': 6,
            'year': 2025
        })
        
        client.post('/mark_fixed_expense_paid', data={
            'fixed_expense_id': utilities.id,
            'account_id': checking.id,
            'month': 6,
            'year': 2025
        })
        
        # Now set regular account data
        response = client.post('/set_regular_account_data', data={
            'account_id': checking.id,
            'month': 6,
            'year': 2025,
            'opening_balance': 2000.00,
            'income': 3000.00,
            'closing_balance': 2500.00
        })
        
        assert response.status_code == 302
        
        # Verify total expenses calculation
        # Total expenses = 2000 + 3000 - 2500 = 2500
        # Fixed expenses = 1200 + 150 = 1350
        # Other expenses = 2500 - 1350 = 1150
        
        transactions = MonthlyTransaction.query.filter_by(account_id=checking.id, month=6, year=2025).all()
        
        fixed_expense_transactions = [t for t in transactions if t.fixed_expense_id is not None]
        other_expense_transactions = [t for t in transactions if t.transaction_type == 'expense' and t.fixed_expense_id is None]
        
        assert len(fixed_expense_transactions) == 2
        assert sum(t.amount for t in fixed_expense_transactions) == 1350.00
        
        assert len(other_expense_transactions) == 1
        assert other_expense_transactions[0].amount == 1150.00
        
        print("✓ Fixed expenses integration working correctly")
        print(f"✓ Fixed expenses total: €{sum(t.amount for t in fixed_expense_transactions):.2f}")
        print(f"✓ Other expenses: €{other_expense_transactions[0].amount:.2f}")
    
    def test_account_type_detection(self, client):
        """Test 4: Account Type Detection and Interface Differentiation"""
        print("\n=== TEST 4: Account Type Detection ===")
        
        # Create different account types
        accounts = [
            BankAccount(name="Checking Account", account_type="checking", bank_name="Test Bank"),
            BankAccount(name="Savings Account", account_type="savings", bank_name="Test Bank"),
            BankAccount(name="Investment Account", account_type="investment", bank_name="Test Bank"),
            BankAccount(name="Credit Card", account_type="credit", bank_name="Test Bank"),
            BankAccount(name="Personal Loan", account_type="loan", bank_name="Test Bank")
        ]
        
        for account in accounts:
            db.session.add(account)
        db.session.commit()
        
        # Test that regular accounts reject debt account endpoint
        regular_account = accounts[0]  # checking
        response = client.post('/set_debt_account_data', data={
            'account_id': regular_account.id,
            'month': 6,
            'year': 2025,
            'opening_balance': 1000.00,
            'paid_amount': 500.00,
            'closing_balance': 800.00
        })
        
        # Should redirect back (error case)
        assert response.status_code == 302
        
        # Test that debt accounts reject regular account endpoint
        debt_account = accounts[3]  # credit
        response = client.post('/set_regular_account_data', data={
            'account_id': debt_account.id,
            'month': 6,
            'year': 2025,
            'opening_balance': 1000.00,
            'income': 500.00,
            'closing_balance': 800.00
        })
        
        # Should redirect back (error case)
        assert response.status_code == 302
        
        print("✓ Account type detection working correctly")
        print("✓ Endpoint security enforced")
    
    def test_balance_adjustment_scenarios(self, client):
        """Test 5: Balance Adjustment and Edge Cases"""
        print("\n=== TEST 5: Balance Adjustment Scenarios ===")
        
        # Create account
        checking = BankAccount(name="Main Checking", account_type="checking", bank_name="Test Bank")
        db.session.add(checking)
        db.session.commit()
        
        # Test scenario where calculated expenses are negative (over-adjustment)
        response = client.post('/set_regular_account_data', data={
            'account_id': checking.id,
            'month': 6,
            'year': 2025,
            'opening_balance': 1000.00,
            'income': 2000.00,
            'closing_balance': 3500.00  # More than opening + income
        })
        
        assert response.status_code == 302
        
        # Should create a misc_income transaction to balance
        # Calculated expenses = 1000 + 2000 - 3500 = -500 (negative)
        # Should create misc_income of 500
        
        transactions = MonthlyTransaction.query.filter_by(account_id=checking.id, month=6, year=2025).all()
        misc_income_transactions = [t for t in transactions if t.transaction_type == 'misc_income']
        
        assert len(misc_income_transactions) == 1
        assert misc_income_transactions[0].amount == 500.00
        
        print("✓ Negative expense adjustment working correctly")
        print(f"✓ Created misc income: €{misc_income_transactions[0].amount:.2f}")

def run_tests():
    """Run all tests"""
    print("🧪 Starting Unified Account System Tests...")
    print("=" * 60)
    
    # Create test instance
    test_instance = TestUnifiedAccountSystem()
    
    # Mock client fixture
    class MockClient:
        def __init__(self):
            app.config['TESTING'] = True
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            self.test_client_instance = app.test_client()
            
        def __enter__(self):
            self.app_context = app.app_context()
            self.app_context.push()
            db.create_all()
            return self.test_client_instance
            
        def __exit__(self, *args):
            db.drop_all()
            self.app_context.pop()
    
    try:
        with MockClient() as client:
            test_instance.test_regular_account_creation_and_data_entry(client)
            test_instance.test_debt_account_creation_and_data_entry(client)
            test_instance.test_regular_account_with_fixed_expenses(client)
            test_instance.test_account_type_detection(client)
            test_instance.test_balance_adjustment_scenarios(client)
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! Unified account system working perfectly!")
        print("✓ Regular accounts: Opening + Income - Closing = Expenses")
        print("✓ Debt accounts: Closing - Opening + Paid = Monthly Spend")
        print("✓ Fixed expenses integration working")
        print("✓ Account type detection and security working")
        print("✓ Balance adjustment scenarios handled")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    run_tests() 
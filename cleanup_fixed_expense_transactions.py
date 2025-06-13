#!/usr/bin/env python3
"""
Script to clean up fixed expense transactions that were affecting balance calculations
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, MonthlyTransaction, FixedExpense, MonthlyBalance

def cleanup_fixed_expense_transactions():
    """Remove all fixed expense transactions and recalculate MonthlyBalance.expenses to exclude them"""
    
    print("🧹 Cleaning Up Fixed Expense Transactions")
    print("=" * 50)
    
    try:
        # Find all transactions that are linked to fixed expenses
        fixed_expense_transactions = MonthlyTransaction.query.filter(
            MonthlyTransaction.fixed_expense_id.isnot(None)
        ).all()
        
        if not fixed_expense_transactions:
            print("✅ No fixed expense transactions found - nothing to clean up!")
            return True
        
        print(f"Found {len(fixed_expense_transactions)} fixed expense transactions to remove:")
        print()
        
        total_amount = 0
        transactions_by_account = {}
        affected_balances = set()
        
        # Group by account and show details
        for transaction in fixed_expense_transactions:
            account_name = transaction.account.name
            if account_name not in transactions_by_account:
                transactions_by_account[account_name] = []
            transactions_by_account[account_name].append(transaction)
            total_amount += transaction.amount
            
            # Track which MonthlyBalance records need recalculation
            affected_balances.add((transaction.account_id, transaction.month, transaction.year))
            
            print(f"📋 {transaction.description} - €{transaction.amount:.2f}")
            print(f"   Account: {account_name} | Month: {transaction.month}/{transaction.year}")
        
        print(f"\n💰 Total amount to be removed from calculations: €{total_amount:.2f}")
        print("\n📊 Breakdown by Account:")
        
        for account_name, transactions in transactions_by_account.items():
            account_total = sum(t.amount for t in transactions)
            print(f"  • {account_name}: €{account_total:.2f} ({len(transactions)} transactions)")
        
        print(f"\n⚡ Found {len(affected_balances)} MonthlyBalance records that need recalculation")
        
        # Ask for confirmation
        response = input("\n🔄 Proceed with cleanup and recalculation? (y/n): ").lower().strip()
        if response != 'y':
            print("❌ Cleanup cancelled by user")
            return False
        
        # Delete all fixed expense transactions
        print("\n🗑️  Deleting fixed expense transactions...")
        for transaction in fixed_expense_transactions:
            db.session.delete(transaction)
        
        # Recalculate MonthlyBalance.expenses for affected records
        print("🔄 Recalculating MonthlyBalance.expenses...")
        recalculated_count = 0
        
        for account_id, month, year in affected_balances:
            balance = MonthlyBalance.query.filter_by(
                account_id=account_id,
                month=month,
                year=year
            ).first()
            
            if balance:
                # Get all remaining transactions (excluding fixed expense transactions)
                remaining_transactions = MonthlyTransaction.query.filter_by(
                    account_id=account_id,
                    month=month,
                    year=year
                ).filter(MonthlyTransaction.fixed_expense_id.is_(None)).all()
                
                # Recalculate expenses from remaining transactions
                old_expenses = balance.expenses
                new_expenses = sum(t.amount for t in remaining_transactions if t.transaction_type in ['expense', 'misc_expense'])
                balance.expenses = new_expenses
                
                print(f"  • Account {account_id} ({month}/{year}): €{old_expenses:.2f} → €{new_expenses:.2f}")
                recalculated_count += 1
        
        # Commit all changes
        db.session.commit()
        
        print(f"\n✅ Cleanup completed successfully!")
        print(f"   • Deleted: {len(fixed_expense_transactions)} fixed expense transactions")
        print(f"   • Recalculated: {recalculated_count} MonthlyBalance records")
        print(f"   • Total amount removed from calculations: €{total_amount:.2f}")
        print("\n🎯 Fixed expenses are now purely for tracking - they won't affect balance calculations!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during cleanup: {str(e)}")
        db.session.rollback()
        return False

if __name__ == "__main__":
    with app.app_context():
        success = cleanup_fixed_expense_transactions()
        if success:
            print("\n🎉 All done! Your expense calculations should now be accurate.")
        else:
            print("\n💔 Cleanup failed. Please check the error and try again.") 
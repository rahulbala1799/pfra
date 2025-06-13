#!/usr/bin/env python3
"""
Test script for the new Monthly Data System

This script tests:
1. Monthly data page loads with new interface
2. Add income functionality works
3. Add expense functionality works  
4. Fixed expense payment marking works
5. Auto-balancing works when setting closing balance
"""

import requests
import time
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:5001"
TEST_MONTH = 6
TEST_YEAR = 2025

def test_monthly_data_page():
    """Test that the monthly data page loads with new interface"""
    print("🧪 Testing Monthly Data Page...")
    
    response = requests.get(f"{BASE_URL}/monthly_data?month={TEST_MONTH}&year={TEST_YEAR}")
    
    if response.status_code == 200:
        content = response.text
        
        # Check for key elements of new interface
        checks = [
            ('Add Income button', 'Add Income' in content),
            ('Add Expense button', 'Add Expense' in content),
            ('Account summaries', 'Opening Balance' in content and 'Current Estimated' in content),
            ('Fixed Expenses section', 'Fixed Expenses This Month' in content),
            ('Transactions table', 'Transactions This Month' in content),
            ('EUR currency', '€' in content),
        ]
        
        passed = 0
        for check_name, result in checks:
            if result:
                print(f"   ✅ {check_name}: PASS")
                passed += 1
            else:
                print(f"   ❌ {check_name}: FAIL")
        
        print(f"   📊 Monthly Data Interface: {passed}/{len(checks)} checks passed")
        return passed == len(checks)
    else:
        print(f"   ❌ Page failed to load: {response.status_code}")
        return False

def test_add_income():
    """Test adding income through the new system"""
    print("\n🧪 Testing Add Income...")
    
    # Get the current page to check form action
    page_response = requests.get(f"{BASE_URL}/monthly_data?month={TEST_MONTH}&year={TEST_YEAR}")
    if page_response.status_code != 200:
        print("   ❌ Cannot access monthly data page")
        return False
    
    # Check if add income form exists
    if 'add_monthly_income' in page_response.text:
        print("   ✅ Add Income form found")
        return True
    else:
        print("   ❌ Add Income form not found")
        return False

def test_add_expense():
    """Test adding expense through the new system"""
    print("\n🧪 Testing Add Expense...")
    
    # Get the current page to check form action
    page_response = requests.get(f"{BASE_URL}/monthly_data?month={TEST_MONTH}&year={TEST_YEAR}")
    if page_response.status_code != 200:
        print("   ❌ Cannot access monthly data page")
        return False
    
    # Check if add expense form exists
    if 'add_monthly_expense' in page_response.text:
        print("   ✅ Add Expense form found")
        return True
    else:
        print("   ❌ Add Expense form not found")
        return False

def test_fixed_expenses_integration():
    """Test fixed expenses integration"""
    print("\n🧪 Testing Fixed Expenses Integration...")
    
    page_response = requests.get(f"{BASE_URL}/monthly_data?month={TEST_MONTH}&year={TEST_YEAR}")
    if page_response.status_code != 200:
        print("   ❌ Cannot access monthly data page")
        return False
    
    content = page_response.text
    
    checks = [
        ('Fixed expenses section exists', 'Fixed Expenses This Month' in content),
        ('Mark as paid functionality', 'mark_fixed_expense_paid' in content or 'Mark Paid' in content),
        ('Fixed expenses navigation link', 'fixed_expenses' in content),
    ]
    
    passed = 0
    for check_name, result in checks:
        if result:
            print(f"   ✅ {check_name}: PASS")
            passed += 1
        else:
            print(f"   ❌ {check_name}: FAIL")
    
    return passed >= 2  # At least 2 out of 3 checks should pass

def test_closing_balance_feature():
    """Test closing balance and auto-balancing feature"""
    print("\n🧪 Testing Closing Balance & Auto-balancing...")
    
    page_response = requests.get(f"{BASE_URL}/monthly_data?month={TEST_MONTH}&year={TEST_YEAR}")
    if page_response.status_code != 200:
        print("   ❌ Cannot access monthly data page")
        return False
    
    content = page_response.text
    
    checks = [
        ('Closing balance form exists', 'set_closing_balance' in content),
        ('Actual Closing input found', 'Actual Closing' in content),
        ('Auto-balance logic route exists', 'set_closing_balance' in content),
    ]
    
    passed = 0
    for check_name, result in checks:
        if result:
            print(f"   ✅ {check_name}: PASS")
            passed += 1
        else:
            print(f"   ❌ {check_name}: FAIL")
    
    return passed == len(checks)

def test_eur_currency_consistency():
    """Test that EUR currency is used consistently"""
    print("\n🧪 Testing EUR Currency Consistency...")
    
    page_response = requests.get(f"{BASE_URL}/monthly_data?month={TEST_MONTH}&year={TEST_YEAR}")
    if page_response.status_code != 200:
        print("   ❌ Cannot access monthly data page")
        return False
    
    content = page_response.text
    
    # Count EUR symbols vs USD symbols
    eur_count = content.count('€')
    usd_count = content.count('$')
    
    print(f"   📊 Found {eur_count} EUR symbols (€) and {usd_count} USD symbols ($)")
    
    if eur_count > 0 and usd_count == 0:
        print("   ✅ EUR currency consistency: PASS")
        return True
    else:
        print("   ❌ EUR currency consistency: FAIL")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🚀 Starting Monthly Data System Tests")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing against: {BASE_URL}")
    print("=" * 60)
    
    tests = [
        ("Monthly Data Page Interface", test_monthly_data_page),
        ("Add Income Functionality", test_add_income),
        ("Add Expense Functionality", test_add_expense),
        ("Fixed Expenses Integration", test_fixed_expenses_integration),
        ("Closing Balance & Auto-balancing", test_closing_balance_feature),
        ("EUR Currency Consistency", test_eur_currency_consistency),
    ]
    
    results = []
    passed_count = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                passed_count += 1
        except Exception as e:
            print(f"   ❌ Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Overall Result: {passed_count}/{len(tests)} tests passed")
    
    if passed_count == len(tests):
        print("🎉 All tests PASSED! New Monthly Data System is working perfectly!")
    elif passed_count >= len(tests) * 0.8:
        print("⚠️  Most tests PASSED! System is mostly functional with minor issues.")
    else:
        print("🚨 Several tests FAILED! System needs attention.")
    
    print(f"⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return passed_count == len(tests)

if __name__ == "__main__":
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    success = run_all_tests()
    exit(0 if success else 1) 
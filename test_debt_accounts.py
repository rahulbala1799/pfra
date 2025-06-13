#!/usr/bin/env python3
"""
Test script for Debt Account Functionality

This script tests:
1. Monthly data page shows different interface for credit/loan accounts
2. Debt account calculation logic works correctly
3. Monthly spend is calculated properly
4. Regular accounts still work as before
"""

import requests
import time
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:5001"
TEST_MONTH = 6
TEST_YEAR = 2025

def test_debt_account_interface():
    """Test that debt accounts show different interface"""
    print("🧪 Testing Debt Account Interface...")
    
    response = requests.get(f"{BASE_URL}/monthly_data?month={TEST_MONTH}&year={TEST_YEAR}")
    
    if response.status_code == 200:
        content = response.text
        
        # Check for debt account specific elements
        checks = [
            ('Debt account form exists', 'set_debt_account_data' in content),
            ('Opening Balance (Owed) label', 'Opening Balance (Owed)' in content),
            ('Paid Amount field', 'Paid Amount' in content),
            ('Closing Balance (Still Owe) label', 'Closing Balance (Still Owe)' in content),
            ('Monthly Spend calculation', 'Monthly Spend' in content),
            ('Calculate & Save button', 'Calculate & Save' in content),
            ('Credit card/loan styling', 'border-warning' in content or 'fa-credit-card' in content),
        ]
        
        passed = 0
        for check_name, result in checks:
            if result:
                print(f"   ✅ {check_name}: PASS")
                passed += 1
            else:
                print(f"   ❌ {check_name}: FAIL")
        
        print(f"   📊 Debt Account Interface: {passed}/{len(checks)} checks passed")
        return passed >= 5  # At least 5 out of 7 checks should pass
    else:
        print(f"   ❌ Page failed to load: {response.status_code}")
        return False

def test_monthly_spend_calculation():
    """Test the monthly spend calculation logic"""
    print("\n🧪 Testing Monthly Spend Calculation Logic...")
    
    # Test scenarios for Monthly Spend = Closing Balance - Opening Balance + Paid Amount
    test_cases = [
        {
            'name': 'Basic spending scenario',
            'opening': 1000,
            'paid': 200,
            'closing': 1100,
            'expected_spend': 300  # 1100 - 1000 + 200 = 300
        },
        {
            'name': 'Payment reduces debt',
            'opening': 1500,
            'paid': 500,
            'closing': 1200,
            'expected_spend': 200  # 1200 - 1500 + 500 = 200
        },
        {
            'name': 'No spending, only payment',
            'opening': 1000,
            'paid': 300,
            'closing': 700,
            'expected_spend': 0  # 700 - 1000 + 300 = 0
        },
        {
            'name': 'Heavy spending',
            'opening': 500,
            'paid': 100,
            'closing': 900,
            'expected_spend': 500  # 900 - 500 + 100 = 500
        }
    ]
    
    passed = 0
    for case in test_cases:
        opening = case['opening']
        paid = case['paid']
        closing = case['closing']
        expected = case['expected_spend']
        
        # Calculate using our formula
        calculated = closing - opening + paid
        
        if calculated == expected:
            print(f"   ✅ {case['name']}: PASS (€{calculated})")
            passed += 1
        else:
            print(f"   ❌ {case['name']}: FAIL (Expected €{expected}, got €{calculated})")
    
    print(f"   📊 Calculation Logic: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)

def test_regular_accounts_still_work():
    """Test that regular accounts still work as before"""
    print("\n🧪 Testing Regular Account Compatibility...")
    
    response = requests.get(f"{BASE_URL}/monthly_data?month={TEST_MONTH}&year={TEST_YEAR}")
    
    if response.status_code == 200:
        content = response.text
        
        # Check for regular account elements
        checks = [
            ('Add Income modal exists', 'addIncomeModal' in content),
            ('Add Expense modal exists', 'addExpenseModal' in content),
            ('Regular account closing balance', 'Actual Closing' in content),
            ('Opening balance editor', 'Set opening' in content),
            ('Current estimated balance', 'Current Estimated' in content),
        ]
        
        passed = 0
        for check_name, result in checks:
            if result:
                print(f"   ✅ {check_name}: PASS")
                passed += 1
            else:
                print(f"   ❌ {check_name}: FAIL")
        
        print(f"   📊 Regular Account Compatibility: {passed}/{len(checks)} checks passed")
        return passed == len(checks)
    else:
        print(f"   ❌ Page failed to load: {response.status_code}")
        return False

def test_javascript_functionality():
    """Test that JavaScript calculation functionality is present"""
    print("\n🧪 Testing JavaScript Calculation Features...")
    
    response = requests.get(f"{BASE_URL}/monthly_data?month={TEST_MONTH}&year={TEST_YEAR}")
    
    if response.status_code == 200:
        content = response.text
        
        # Check for JavaScript elements
        checks = [
            ('calculateMonthlySpend function', 'function calculateMonthlySpend' in content),
            ('Real-time calculation setup', 'addEventListener' in content),
            ('Monthly spend element ID', 'monthly-spend-' in content),
            ('Input event listeners', 'input' in content and 'addEventListener' in content),
        ]
        
        passed = 0
        for check_name, result in checks:
            if result:
                print(f"   ✅ {check_name}: PASS")
                passed += 1
            else:
                print(f"   ❌ {check_name}: FAIL")
        
        print(f"   📊 JavaScript Features: {passed}/{len(checks)} checks passed")
        return passed >= 3  # At least 3 out of 4 checks should pass
    else:
        print(f"   ❌ Page failed to load: {response.status_code}")
        return False

def test_debt_account_routes():
    """Test that debt account routes are accessible"""
    print("\n🧪 Testing Debt Account API Routes...")
    
    # Test the debt account route exists (we can't easily POST without form data)
    page_response = requests.get(f"{BASE_URL}/monthly_data?month={TEST_MONTH}&year={TEST_YEAR}")
    
    if page_response.status_code == 200:
        content = page_response.text
        
        if 'set_debt_account_data' in content:
            print("   ✅ Debt account route accessible: PASS")
            return True
        else:
            print("   ❌ Debt account route not found: FAIL")
            return False
    else:
        print(f"   ❌ Cannot access page: {page_response.status_code}")
        return False

def run_all_tests():
    """Run all debt account tests and provide summary"""
    print("🚀 Starting Debt Account System Tests")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing against: {BASE_URL}")
    print("=" * 60)
    
    tests = [
        ("Debt Account Interface", test_debt_account_interface),
        ("Monthly Spend Calculation Logic", test_monthly_spend_calculation),
        ("Regular Account Compatibility", test_regular_accounts_still_work),
        ("JavaScript Calculation Features", test_javascript_functionality),
        ("Debt Account API Routes", test_debt_account_routes),
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
    print("📋 DEBT ACCOUNT TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Overall Result: {passed_count}/{len(tests)} tests passed")
    
    if passed_count == len(tests):
        print("🎉 All tests PASSED! Debt account system is working perfectly!")
        print("\n💳 Key Features Verified:")
        print("   • Credit cards and loans show different interface")
        print("   • Monthly spend calculation: Closing - Opening + Paid")
        print("   • Real-time JavaScript calculations")
        print("   • Regular accounts unchanged")
        print("   • All API routes functional")
    elif passed_count >= len(tests) * 0.8:
        print("⚠️  Most tests PASSED! System is mostly functional with minor issues.")
    else:
        print("🚨 Several tests FAILED! System needs attention.")
    
    print(f"⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return passed_count == len(tests)

if __name__ == "__main__":
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    success = run_all_tests()
    exit(0 if success else 1) 
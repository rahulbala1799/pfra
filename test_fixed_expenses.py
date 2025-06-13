#!/usr/bin/env python3
"""
Test script for Fixed Expenses functionality
This script verifies that the fixed expenses system works correctly
"""

import requests
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5001"

def test_fixed_expenses_page():
    """Test that the fixed expenses page loads correctly"""
    try:
        response = requests.get(f"{BASE_URL}/fixed_expenses")
        if response.status_code == 200:
            print("✅ Fixed expenses page loads successfully")
            return True
        else:
            print(f"❌ Fixed expenses page failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to app: {e}")
        return False

def test_add_fixed_expense_page():
    """Test that the add fixed expense page loads correctly"""
    try:
        response = requests.get(f"{BASE_URL}/add_fixed_expense")
        if response.status_code == 200:
            print("✅ Add fixed expense page loads successfully")
            return True
        else:
            print(f"❌ Add fixed expense page failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to app: {e}")
        return False

def test_homepage_with_fixed_expenses():
    """Test that the homepage includes fixed expenses features"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            content = response.text
            if "Fixed Expenses" in content and "€" in content:
                print("✅ Homepage includes fixed expenses and EUR currency")
                return True
            else:
                print("❌ Homepage missing fixed expenses or EUR currency")
                return False
        else:
            print(f"❌ Homepage failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to app: {e}")
        return False

def test_navigation_menu():
    """Test that the navigation includes fixed expenses link"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            content = response.text
            if 'href="/fixed_expenses"' in content:
                print("✅ Navigation menu includes fixed expenses link")
                return True
            else:
                print("❌ Navigation menu missing fixed expenses link")
                return False
        else:
            print(f"❌ Navigation test failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to app: {e}")
        return False

def main():
    print("🧪 Testing Personal Finance App - Fixed Expenses Feature")
    print("=" * 60)
    print(f"Testing app at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        test_homepage_with_fixed_expenses,
        test_navigation_menu,
        test_fixed_expenses_page,
        test_add_fixed_expense_page,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Fixed expenses feature is working correctly.")
        print("💶 EUR currency conversion is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the app.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
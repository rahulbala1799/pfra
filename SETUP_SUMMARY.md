# Personal Finance App - Setup Summary

## 🎯 **PERMANENT RULES** (NEVER CHANGE)

### 1. **EUR Currency Rule** 💶
- **ALL financial data MUST be in EUR (€)**
- This includes: bank balances, income, expenses, fixed expenses, charts, forms
- Currency symbol: € (not $, £, or any other currency)
- Maintained in: templates, database, charts, JavaScript

### 2. **Port 5001 Management Rule** 🔌
- **ALWAYS kill port 5001 processes before starting the app**
- Command: `lsof -ti:5001 | xargs kill -9`
- Use startup script: `./start_app.sh` (recommended)
- Prevents "Address already in use" errors

## 🏗️ **Architecture Overview**

### Database Models (SQLite)
1. **BankAccount** - Multiple bank accounts (savings, checking, credit, investment)
2. **MonthlyBalance** - Monthly financial data per account
3. **FixedExpense** - Recurring expenses (monthly/quarterly/yearly)
4. **Category** - Income/expense categories
5. **MonthlyCategory** - Category amounts per month

### Key Features
- ✅ Monthly balance tracking (not individual transactions)
- ✅ Fixed expenses management with frequency support
- ✅ Interactive charts and analytics (12-month trends)
- ✅ Stock market analysis
- ✅ EUR currency throughout
- ✅ SQLite database with proper relationships
- ✅ Bootstrap 5 responsive UI

## 🚀 **Quick Start Commands**

### Option A: Automated (Recommended)
```bash
./start_app.sh
```

### Option B: Manual
```bash
# Kill port 5001 processes
lsof -ti:5001 | xargs kill -9

# Activate environment and start
source venv/bin/activate
python app.py
```

### Test the Application
```bash
python test_fixed_expenses.py
```

## 📊 **App URLs & Navigation**

- **Homepage**: http://localhost:5001/
- **Accounts**: http://localhost:5001/accounts
- **Monthly Data**: http://localhost:5001/monthly_data
- **Fixed Expenses**: http://localhost:5001/fixed_expenses ⭐ NEW
- **Dashboard**: http://localhost:5001/dashboard
- **Stocks**: http://localhost:5001/stocks

## 🆕 **Fixed Expenses Feature**

### What it does:
- Tracks recurring monthly expenses (rent, subscriptions, utilities)
- Supports monthly, quarterly, and yearly frequencies
- Calculates monthly impact for budget planning
- Manages active/inactive status
- Provides comprehensive expense overview

### Pages:
1. **Main Page** (`/fixed_expenses`): Summary cards + expense tables
2. **Add Form** (`/add_fixed_expense`): Comprehensive expense creation
3. **Edit Form** (`/edit_fixed_expense/<id>`): Update existing expenses

### Key Features:
- Real-time monthly impact calculation
- Category management (Housing, Utilities, Subscriptions, etc.)
- Date range support (start/end dates)
- Frequency conversion to monthly equivalents
- Active/inactive status toggle

## 💶 **EUR Currency Implementation**

### Where EUR is used:
- All form labels: "Amount (€)"
- All displays: €1,234.56
- Chart axis labels: "Amount (€)"
- Summary cards and metrics
- Database amount fields
- JavaScript calculations

### Files Updated:
- `app.py` - Chart functions, database models
- All `templates/*.html` - Currency symbols and labels
- `README.md` - Documentation
- Startup scripts and tests

## 🔧 **Development Guidelines**

### When adding new features:
1. ✅ Use EUR (€) for ALL financial amounts
2. ✅ Kill port 5001 before testing
3. ✅ Follow SQLite database structure
4. ✅ Use Bootstrap 5 for UI consistency
5. ✅ Add proper form validation
6. ✅ Include responsive design
7. ✅ Test with `test_fixed_expenses.py`

### File naming conventions:
- Templates: `snake_case.html`
- Routes: `/snake_case` 
- Database models: `CamelCase`
- JavaScript functions: `camelCase`

## 📁 **Key Files**

| File | Purpose |
|------|---------|
| `app.py` | Main Flask app with EUR rule comment |
| `start_app.sh` | Startup script with port management |
| `test_fixed_expenses.py` | Feature testing script |
| `templates/fixed_expenses.html` | Main fixed expenses page |
| `templates/add_fixed_expense.html` | Add expense form |
| `templates/edit_fixed_expense.html` | Edit expense form |
| `personal_finance.db` | SQLite database |
| `README.md` | Updated documentation |

## ✅ **Success Verification**

App is working correctly when:
- ✅ All pages load without errors
- ✅ Navigation includes "Fixed Expenses" 
- ✅ All amounts show € symbol
- ✅ Fixed expenses can be added/edited
- ✅ Monthly impact calculations work
- ✅ Charts display EUR currency
- ✅ Test script passes 4/4 tests

## 🔄 **Future Development**

When extending the app:
- Maintain EUR currency in ALL new features
- Use the FixedExpense model as reference for new database models
- Follow the monthly-based approach (not individual transactions)
- Always test with the startup script
- Update test script for new features
- Keep responsive Bootstrap 5 design

---

**Created**: June 2025  
**Status**: Production Ready  
**Currency**: EUR (€) Only  
**Port**: 5001 (with auto-kill rule) 
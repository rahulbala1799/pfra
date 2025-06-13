# Personal Finance Flask App

A comprehensive personal finance management application built with Python Flask, featuring monthly balance tracking, fixed expense management, data visualization, and stock market analysis. **All financial data is tracked in EUR (€)**.

## Features

- 🏦 **Bank Account Management**: Track multiple accounts (savings, checking, credit, investment)
- 📅 **Monthly Balance Tracking**: Record opening/closing balances, income, and expenses by month
- 💸 **Fixed Expenses Management**: Track recurring monthly, quarterly, and yearly expenses
- 📊 **Interactive Dashboard**: Financial overview with charts and analytics using Plotly
- 📈 **Stock Market Analysis**: Real-time stock price tracking and analysis
- 💶 **EUR Currency**: All amounts displayed and tracked in Euros (€)
- 🗄️ **SQLite Database**: Secure local data storage with proper relationships
- 🎨 **Modern UI**: Clean, responsive design with Bootstrap 5

## Tech Stack

- **Backend**: Python Flask
- **Data Analysis**: Pandas, NumPy, Scikit-learn
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Forecasting**: Prophet, Statsmodels
- **Stock Data**: yFinance
- **Frontend**: Bootstrap 5, Font Awesome, jQuery
- **Charts**: Plotly.js

## Installation

1. **Clone or download the project files**

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   **Option A: Using the startup script (Recommended)**
   ```bash
   ./start_app.sh
   ```

   **Option B: Manual startup**
   ```bash
   # PERMANENT RULE: Always kill port 5001 processes first
   lsof -ti:5001 | xargs kill -9
   source venv/bin/activate
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5001`

### ⚠️ **PERMANENT RULE: Port 5001 Management**

**Always kill any processes running on port 5001 before starting the app.** This prevents "Address already in use" errors that can occur when the app was previously terminated unexpectedly.

The startup script `start_app.sh` automatically handles this for you.

## Usage

### Managing Bank Accounts
- Navigate to "Accounts" from the main menu
- Add multiple accounts (savings, checking, credit, investment)
- Track account details and status

### Simplified Monthly Data Entry (NEW!)
- **Easy Income/Expense Entry**: Simple "Add Income" and "Add Expense" buttons with bank account selection
- **Individual Transaction Tracking**: Each income and expense is recorded as a separate transaction
- **Fixed Expenses Integration**: Mark recurring fixed expenses as paid and select which account they were paid from
- **Auto-Balancing**: Set actual closing balance - any difference is automatically balanced with misc income/expense
- **Opening Balance Management**: Easily set opening balances for each account per month
- **Real-time Calculations**: See estimated current balance based on opening balance + income - expenses
- **Debt Account Support**: Credit cards and loans have specialized interface with opening balance, paid amount, closing balance, and auto-calculated monthly spend

### Fixed Expenses Management
- Navigate to "Fixed Expenses" from the main menu
- Add recurring expenses (monthly, quarterly, yearly)
- Set start/end dates for temporary expenses
- View monthly impact calculations
- Manage active/inactive status

### Dashboard & Analytics
- View comprehensive financial overview
- Interactive charts showing trends over 12 months
- Net worth tracking and growth analysis
- All amounts displayed in EUR (€)

### Forecasting
- Requires at least 10 transactions for basic forecasting
- Uses linear regression to predict future spending
- More data = better accuracy

### Stock Analysis
- Enter any stock symbol (e.g., AAPL, GOOGL, MSFT)
- View 1-year price history
- See current price and performance metrics
- Quick access to popular stocks

### CSV Import
- Upload CSV files with transaction data
- Required columns: date, type, category, description, amount
- Bulk import for historical data

## CSV Format

For importing transactions, use this CSV format:

```csv
date,type,category,description,amount
2023-01-01,expense,food,Grocery shopping,45.67
2023-01-02,income,salary,Monthly salary,3000.00
2023-01-03,expense,transportation,Gas,30.00
```

## Dependencies

### Core Dependencies
- Flask==2.3.3
- pandas==2.1.1
- numpy==1.24.3

### Data Analysis & ML
- scikit-learn==1.3.0
- scipy==1.11.2
- statsmodels==0.14.0
- prophet==1.1.4

### Visualization
- matplotlib==3.7.2
- seaborn==0.12.2
- plotly==5.16.1

### Financial Data
- yfinance==0.2.22

### File Processing
- openpyxl==3.1.2
- xlrd==2.0.1

## Project Structure

```
pfra/
├── app.py                      # Main Flask application (EUR currency + fixed expenses)
├── start_app.sh               # Startup script (kills port 5001, starts app)
├── test_fixed_expenses.py     # Test script for fixed expenses feature
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── personal_finance.db        # SQLite database
├── venv/                      # Virtual environment
├── templates/                 # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Home page (EUR + fixed expenses)
│   ├── dashboard.html         # Financial dashboard (EUR charts)
│   ├── accounts.html          # Bank accounts management
│   ├── add_account.html       # Add bank account form
│   ├── monthly_data.html      # Monthly balance tracking (EUR)
│   ├── fixed_expenses.html    # Fixed expenses management
│   ├── add_fixed_expense.html # Add fixed expense form
│   ├── edit_fixed_expense.html# Edit fixed expense form
│   ├── stocks.html            # Stock market analysis
│   ├── add_transaction.html   # Legacy transaction form
│   └── transactions.html      # Legacy transactions view
└── uploads/                   # CSV upload directory (if needed)
```

## API Endpoints

- `GET /` - Home page
- `GET /dashboard` - Financial dashboard
- `GET/POST /add_transaction` - Add new transaction
- `GET /transactions` - View all transactions
- `GET /forecast` - Financial forecasting
- `GET /stocks` - Stock market analysis
- `GET /api/stock_data/<symbol>` - Stock data API
- `POST /upload_csv` - CSV file upload

## Development

### Running in Development Mode
The app runs in debug mode by default when executed directly:

```bash
python app.py
```

### Production Deployment
For production, use a WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] User authentication and multiple accounts
- [ ] Advanced budgeting features
- [ ] Investment portfolio tracking
- [ ] Bill reminders and notifications
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced forecasting with Prophet
- [ ] Export to PDF reports
- [ ] Bank account integration
- [ ] Cryptocurrency tracking

## Contributing

Feel free to contribute by:
1. Reporting bugs
2. Suggesting new features
3. Submitting pull requests
4. Improving documentation

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Common Issues

1. **Prophet Installation Issues**:
   ```bash
   # On macOS
   brew install cmake
   pip install prophet
   
   # On Linux
   sudo apt-get install build-essential
   pip install prophet
   ```

2. **Port Already in Use**:
   - Change the port in `app.py`: `app.run(port=5001)`
   - Or kill the process using the port

3. **Module Not Found**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check if you're using the correct Python environment

4. **CSV Upload Issues**:
   - Ensure CSV has required columns: date, type, category, description, amount
   - Check date format (YYYY-MM-DD recommended)

## Support

For questions or issues, please:
1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Create an issue with detailed error messages

---

**Happy Financial Tracking! 💰📊** 
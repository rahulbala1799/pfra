#!/bin/bash

# Personal Finance Flask App Startup Script
# 
# PERMANENT RULE: Always kill port 5001 processes before starting the app
# This prevents "Address already in use" errors

echo "🔥 Killing any processes on port 5001..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || echo "No processes found on port 5001"

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "🚀 Starting Personal Finance Flask App..."
echo "💶 All transactions are tracked in EUR (€)"
echo "📊 Fixed expenses management available"
echo ""
echo "🌐 App will be available at:"
echo "   - http://localhost:5001"
echo "   - http://127.0.0.1:5001"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

python app.py 
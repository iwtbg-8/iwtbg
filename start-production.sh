#!/bin/bash

# iwtbg Production Startup Script

echo "=========================================="
echo "🎬 iwtbg - Production Mode"
echo "=========================================="
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then run: source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Start the production server
echo "🚀 Starting production server with Waitress..."
echo "📍 Server URL: http://localhost:5000"
echo ""
echo "To stop the server, press Ctrl+C"
echo "=========================================="
echo ""

python3 server_production.py

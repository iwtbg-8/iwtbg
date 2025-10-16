#!/bin/bash

# iwtbg Startup Script

echo "=========================================="
echo "🎬 iwtbg - Starting Services"
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

# Start the Flask backend server
echo "🚀 Starting Flask backend server..."
echo "📍 Backend API: http://localhost:5000"
echo ""
echo "To stop the server, press Ctrl+C"
echo "=========================================="
echo ""

python3 server.py

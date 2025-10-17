#!/usr/bin/env python3
"""
Production server for Video Downloader
Uses Waitress WSGI server instead of Flask development server
"""

from waitress import serve
from server import app
import os
import sys

if __name__ == '__main__':
    # Get port from environment variable (for deployment platforms like Render)
    port = int(os.environ.get('PORT', 10000))
    
    # Debug: Print environment info
    print("=" * 60)
    print("🚀 iwtbg - Production Server Starting")
    print("=" * 60)
    print(f"🔍 PORT environment variable: {os.environ.get('PORT', 'Not set')}")
    print(f"🔍 Binding to port: {port}")
    print(f"🔍 Python version: {sys.version}")
    print(f"🔍 Working directory: {os.getcwd()}")
    
    # Get download directory
    DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
    
    # Create downloads directory if it doesn't exist
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        print(f"📁 Created download directory: {DOWNLOAD_DIR}")
    else:
        print(f"📁 Download directory exists: {DOWNLOAD_DIR}")
    
    print("=" * 60)
    print("\n🌐 Available endpoints:")
    print("  GET  /                 - Frontend website")
    print("  GET  /api              - API status")
    print("  POST /api/analyze      - Analyze video URL")
    print("  POST /api/formats      - Get available formats")
    print("  POST /api/download     - Download video")
    print("=" * 60)
    print(f"\n✨ Starting Waitress server on 0.0.0.0:{port}")
    print("=" * 60)
    
    # Run production server with explicit binding
    try:
        serve(app, host='0.0.0.0', port=port, threads=4, _quiet=False)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

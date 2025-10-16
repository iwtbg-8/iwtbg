#!/usr/bin/env python3
"""
Production server for Video Downloader
Uses Waitress WSGI server instead of Flask development server
"""

from waitress import serve
from server import app
import os

if __name__ == '__main__':
    # Get download directory
    DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
    
    print("=" * 60)
    print("🚀 iwtbg - Production Server")
    print("=" * 60)
    print(f"📁 Download directory: {DOWNLOAD_DIR}")
    print(f"🌐 Server running on: http://localhost:5500")
    print("=" * 60)
    print("\nAvailable endpoints:")
    print("  GET  /                 - Frontend website")
    print("  GET  /api              - API status")
    print("  POST /api/analyze      - Analyze video URL")
    print("  POST /api/formats      - Get available formats")
    print("  POST /api/download     - Download video")
    print("=" * 60)
    print("\n✨ Production server running with Waitress")
    print("Press Ctrl+C to stop the server\n")
    
    # Run production server
    serve(app, host='0.0.0.0', port=5500, threads=4)

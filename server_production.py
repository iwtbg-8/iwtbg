#!/usr/bin/env python3
"""
Production server for Video Downloader
Uses Waitress WSGI server instead of Flask development server
"""

from waitress import serve
from server import app
import os

if __name__ == '__main__':
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get('PORT', 5500))
    
    # Get download directory
    DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
    
    print("=" * 60)
    print("🚀 iwtbg - Production Server")
    print("=" * 60)
    print(f"📁 Download directory: {DOWNLOAD_DIR}")
    print(f"🌐 Server running on: http://0.0.0.0:{port}")
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
    serve(app, host='0.0.0.0', port=port, threads=4)

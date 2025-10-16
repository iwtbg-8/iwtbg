#!/usr/bin/env python3
"""
Test Flask app functionality
"""
from werkzeug.test import Client
from werkzeug.serving import WSGIRequestHandler
import sys
sys.path.insert(0, '/home/kali/Desktop/iwtbg')

from server import app

# Create test client
client = app.test_client()

print("=" * 70)
print("Testing HTTP Methods on Endpoints")
print("=" * 70)
print()

tests = [
    ("GET", "/api", "Should work - GET is allowed"),
    ("GET", "/api/analyze", "Should return 405 - POST required"),
    ("POST", "/api/analyze", "Should return 400 - missing data"),
    ("GET", "/api/download", "Should return 405 - POST required"),
    ("GET", "/test.html", "Should try to serve file"),
]

for method, url, description in tests:
    print(f"\nTest: {method} {url}")
    print(f"Expected: {description}")
    
    if method == "GET":
        response = client.get(url)
    elif method == "POST":
        response = client.post(url, json={})
    
    print(f"Status: {response.status_code} {response.status}")
    if response.is_json:
        print(f"Response: {response.json}")
    print("-" * 70)

print("\n✓ All tests complete!")

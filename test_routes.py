#!/usr/bin/env python3
"""
Test script to verify Flask routes are correctly ordered
"""
import sys
sys.path.insert(0, '/home/kali/Desktop/iwtbg')

from server import app

print("=" * 60)
print("Flask Route Order Test")
print("=" * 60)
print()

# Get all routes
routes = []
for rule in app.url_map.iter_rules():
    methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
    routes.append((rule.rule, methods, rule.endpoint))

# Sort by rule to see order
print("All registered routes:")
print(f"{'Rule':<40} {'Methods':<15} {'Endpoint'}")
print("-" * 70)
for rule, methods, endpoint in sorted(routes):
    print(f"{rule:<40} {methods:<15} {endpoint}")

print()
print("=" * 60)
print("Testing route matching:")
print("=" * 60)

# Test which route matches /api/analyze
test_urls = [
    '/api',
    '/api/analyze',
    '/api/download',
    '/scripts.js',
    '/test.html'
]

with app.test_request_context():
    for url in test_urls:
        try:
            adapter = app.url_map.bind('localhost')
            endpoint, values = adapter.match(url, method='GET')
            print(f"{url:<30} -> {endpoint}")
        except Exception as e:
            print(f"{url:<30} -> ERROR: {e}")

print()
print("✓ Route order test complete!")

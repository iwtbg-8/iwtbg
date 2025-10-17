#!/usr/bin/env python3
import requests
import json
import time

# Wait for server to start
time.sleep(2)

# Test the analyze endpoint
url = 'http://localhost:5000/api/analyze'
data = {'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}

print("Testing YouTube URL analysis...")
try:
    response = requests.post(url, json=data, timeout=30)
    print(f'Status Code: {response.status_code}')

    if response.status_code == 200:
        result = response.json()
        print(f'Success: {result.get("success", False)}')
        if result.get('success'):
            print(f'Title: {result.get("title", "Unknown")}')
            print(f'Duration: {result.get("duration", 0)} seconds')
            print('✓ API working correctly')
        else:
            print(f'Error: {result.get("error", "Unknown error")}')
    elif response.status_code == 500:
        print('✗ HTTP 500 error occurred!')
        print(f'Response: {response.text}')
    else:
        print(f'Other status: {response.status_code}')
        print(f'Response: {response.text}')

except Exception as e:
    print(f'Request failed: {e}')
    import traceback
    traceback.print_exc()
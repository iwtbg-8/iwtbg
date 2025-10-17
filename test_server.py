#!/usr/bin/env python3
import subprocess
import time
import requests
import json
import signal
import os

def test_api():
    # Start server
    print("Starting server...")
    server_process = subprocess.Popen(['python3', 'server.py'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    cwd='/home/kali/Desktop/iwtbg')

    # Wait for server to start
    time.sleep(3)

    try:
        # Test the API
        print("Testing API...")
        url = 'http://localhost:5000/api/analyze'
        data = {'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}

        response = requests.post(url, json=data, timeout=30)
        print(f'Status Code: {response.status_code}')

        if response.status_code == 200:
            result = response.json()
            print(f'Success: {result.get("success", False)}')
            if result.get('success'):
                print(f'Title: {result.get("title", "Unknown")}')
                print('✓ API working correctly')
            else:
                print(f'Error: {result.get("error", "Unknown error")}')
        elif response.status_code == 500:
            print('✗ HTTP 500 error occurred!')
            print(f'Response: {response.text}')
        else:
            print(f'Other status: {response.status_code}')
            print(f'Response: {response.text[:200]}...')

    except Exception as e:
        print(f'Request failed: {e}')
    finally:
        # Kill server
        print("Stopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == '__main__':
    test_api()
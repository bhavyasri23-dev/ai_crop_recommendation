#!/usr/bin/env python3

import requests
import json

def test_api_district_fix():
    """Test the API with different district formats"""

    test_cases = [
        {'district': 'anantapur', 'nitrogen': 60, 'phosphorus': 40, 'pH': 6.5, 'rainfall': 800},
        {'district': 'Anantapur, Andhra Pradesh', 'nitrogen': 60, 'phosphorus': 40, 'pH': 6.5, 'rainfall': 800},
        {'district': 'vizag', 'nitrogen': 60, 'phosphorus': 40, 'pH': 6.5, 'rainfall': 800},
        {'district': 'Vizag, Andhra Pradesh', 'nitrogen': 60, 'phosphorus': 40, 'pH': 6.5, 'rainfall': 800}
    ]

    print("Testing API district normalization fix...")
    print("=" * 50)

    for i, payload in enumerate(test_cases):
        try:
            response = requests.post('http://localhost:5001/api/recommend_crop', json=payload, timeout=5)
            print(f'Test {i+1}: "{payload["district"]}" -> Status: {response.status_code}')
            if response.status_code == 200:
                data = response.json()
                recommendation = data["data"][0]["recommendation"]
                accuracy = data["data"][0]["accuracy"]
                print(f'  ✅ Success: {recommendation} ({accuracy}%)')
            else:
                print(f'  ❌ Error: {response.text}')
        except Exception as e:
            print(f'Test {i+1}: "{payload["district"]}" -> Connection failed: {e}')
        print()

if __name__ == "__main__":
    test_api_district_fix()

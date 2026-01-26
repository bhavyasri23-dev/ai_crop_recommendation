import requests
import json

# Test the API
url = "http://localhost:5002/api/recommend_crop"
payload = {
    "district": "Prakasam",
    "nitrogen": 52,
    "phosphorus": 160,
    "pH": 7.3,
    "rainfall": 780
}

print("Testing API with payload:", payload)

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

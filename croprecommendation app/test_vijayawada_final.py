import requests
import json

# Test Vijayawada with the API
url = "http://localhost:5002/api/recommend_crop"
data = {
    "district": "Vijayawada",
    "nitrogen": 80,
    "phosphorus": 40,
    "pH": 7.0,
    "rainfall": 900
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS: Vijayawada is now accepted by the API")
        print("Response:", json.dumps(result, indent=2))
    else:
        print(f"ERROR: Status code {response.status_code}")
        print("Response:", response.text)
except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect to the backend server. Make sure it's running on port 5002.")
    print("Try running: python crop_recommendation_module/app.py")
except Exception as e:
    print(f"ERROR: {e}")

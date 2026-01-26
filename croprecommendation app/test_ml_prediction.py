import requests
import json

# Test data for non-Andhra Pradesh location (e.g., Punjab region)
test_data = {
    'N': 80,
    'P': 40,
    'K': 40,
    'temperature': 28,
    'humidity': 65,
    'ph': 6.5,
    'rainfall': 120,
    'latitude': 30.0,  # Punjab region (not Andhra Pradesh)
    'longitude': 75.0
}

try:
    response = requests.post('http://localhost:5000/api/predict_crop', json=test_data)
    if response.status_code == 200:
        result = response.json()
        print('Prediction result:')
        print(f'Crop: {result["predicted_crop"]}')
        print(f'Confidence: {result["confidence"]}%')
        print(f'Alternatives: {result["alternatives"]}')
    else:
        print(f'Error: {response.status_code} - {response.text}')
except Exception as e:
    print(f'Error making request: {e}')

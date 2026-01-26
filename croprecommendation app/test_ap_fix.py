import requests
import json

# Test data for Andhra Pradesh location (e.g., Vijayawada coordinates)
test_data = {
    'N': 80,
    'P': 40,
    'K': 40,
    'temperature': 28,
    'humidity': 65,
    'ph': 6.5,
    'rainfall': 120,
    'latitude': 16.5062,  # Vijayawada, Andhra Pradesh
    'longitude': 80.6480
}

print('Testing crop prediction for Andhra Pradesh location...')
print(f'Location: {test_data["latitude"]}, {test_data["longitude"]}')

try:
    response = requests.post('http://localhost:5000/api/predict_crop', json=test_data)
    if response.status_code == 200:
        result = response.json()
        print(f'Predicted crop: {result["predicted_crop"]}')
        print(f'Confidence: {result["confidence"]}%')
        print('Alternatives:')
        for alt in result['alternatives']:
            print(f'  - {alt["crop"]}: {alt["confidence"]}%')
    else:
        print(f'Error: {response.status_code} - {response.text}')
except Exception as e:
    print(f'Connection error: {e}')
    print('Make sure the Flask server is running on port 5000')

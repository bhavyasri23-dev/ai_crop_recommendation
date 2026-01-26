import sys
import os
sys.path.insert(0, 'crop_recommendation_module')
from app import app
import json

def test_sensor_conversion():
    print("Testing IoT Sensor Data Conversion...")

    # Test with sensor_id
    test_data = {
        'sensor_id': 'ASU-AP-04-Guntur',
        'district': 'Guntur'
    }

    with app.test_client() as client:
        response = client.post('/api/recommend_crop',
                              data=json.dumps(test_data),
                              content_type='application/json')
        print('Sensor ID test response:')
        print(response.get_json())
        print()

    # Test with direct sensor_data
    test_data2 = {
        'sensor_data': {
            'pH': 6.5,
            'nitrogen': 50,
            'phosphorus': 30,
            'rainfall': 100
        },
        'district': 'Krishna'
    }

    with app.test_client() as client:
        response = client.post('/api/recommend_crop',
                              data=json.dumps(test_data2),
                              content_type='application/json')
        print('Direct sensor_data test response:')
        print(response.get_json())
        print()

    # Test fallback to manual data
    test_data3 = {
        'pH': 7.0,
        'nitrogen': 60,
        'phosphorus': 40,
        'rainfall': 120,
        'district': 'East Godavari'
    }

    with app.test_client() as client:
        response = client.post('/api/recommend_crop',
                              data=json.dumps(test_data3),
                              content_type='application/json')
        print('Manual data fallback test response:')
        print(response.get_json())

if __name__ == '__main__':
    test_sensor_conversion()

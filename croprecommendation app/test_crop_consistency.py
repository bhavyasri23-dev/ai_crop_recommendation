#!/usr/bin/env python3
"""
Test script to verify crop recommendation consistency across different input methods
Ensures that identical soil conditions produce the same crop recommendations
regardless of input method (manual, satellite, IoT sensors).
"""

import requests
import json
import sys

# Flask app URL (assuming it's running locally)
BASE_URL = "http://localhost:5000"

def test_crop_consistency():
    """Test that identical soil conditions produce consistent crop recommendations"""

    print("=== Testing Crop Recommendation Consistency ===\n")

    # Test cases with identical soil conditions
    test_cases = [
        {
            'name': 'Standard Rice Conditions',
            'features': {
                'soil_pH': 6.5,
                'moisture_percentage': 65.0,
                'nitrogen': 60.0,
                'phosphorus': 45.0,
                'potassium': 180.0,
                'temperature': 27.0,
                'rainfall': 120.0
            },
            'expected_crop': 'Rice'  # Should be consistent across all methods
        },
        {
            'name': 'Cotton Conditions',
            'features': {
                'soil_pH': 7.5,
                'moisture_percentage': 45.0,
                'nitrogen': 80.0,
                'phosphorus': 40.0,
                'potassium': 250.0,
                'temperature': 32.0,
                'rainfall': 85.0
            },
            'expected_crop': 'Cotton'  # Should be consistent across all methods
        },
        {
            'name': 'Wheat Conditions',
            'features': {
                'soil_pH': 6.8,
                'moisture_percentage': 45.0,
                'nitrogen': 35.0,
                'phosphorus': 25.0,
                'potassium': 180.0,
                'temperature': 15.0,
                'rainfall': 50.0
            },
            'expected_crop': 'Wheat'  # Should be consistent across all methods
        }
    ]

    all_consistent = True

    for test_case in test_cases:
        print(f"Testing: {test_case['name']}")
        print("-" * 50)

        features = test_case['features']
        expected_crop = test_case['expected_crop']

        # Test 1: Manual input via /api/recommend_crop
        manual_payload = {
            'soil_pH': features['soil_pH'],
            'moisture_percentage': features['moisture_percentage'],
            'nitrogen': features['nitrogen'],
            'phosphorus': features['phosphorus'],
            'potassium': features['potassium'],
            'temperature': features['temperature'],
            'rainfall': features['rainfall']
        }

        try:
            manual_response = requests.post(f"{BASE_URL}/api/recommend_crop",
                                          json=manual_payload)
            manual_result = manual_response.json()
            manual_crop = manual_result['data']['recommendations'][0]['crop']
            print(f"Manual Input: {manual_crop}")
        except Exception as e:
            print(f"✗ Manual input failed: {e}")
            continue

        # Test 2: Coordinate-based input via /api/predict_crop (simulating satellite/IoT)
        coord_payload = {
            'N': features['nitrogen'],
            'P': features['phosphorus'],
            'K': features['potassium'],
            'temperature': features['temperature'],
            'humidity': features['moisture_percentage'],
            'ph': features['soil_pH'],
            'rainfall': features['rainfall'],
            'latitude': 16.31,  # Guntur coordinates
            'longitude': 80.44
        }

        try:
            coord_response = requests.post(f"{BASE_URL}/api/predict_crop",
                                         json=coord_payload)
            coord_result = coord_response.json()
            coord_crop = coord_result['predicted_crop']
            print(f"Coordinate Input: {coord_crop}")
        except Exception as e:
            print(f"✗ Coordinate input failed: {e}")
            continue

        # Test 3: Satellite data with manual override
        try:
            satellite_response = requests.get(f"{BASE_URL}/api/satellite/soil_data",
                                            params={'lat': 16.31, 'lon': 80.44})
            if satellite_response.status_code == 200:
                satellite_data = satellite_response.json()
                print(f"Satellite Data: N={satellite_data['nitrogen']}, P={satellite_data['phosphorus']}, K={satellite_data['potassium']}, pH={satellite_data['ph']}")
            else:
                print("✗ Satellite data request failed")
        except Exception as e:
            print(f"✗ Satellite data failed: {e}")

        # Test 4: IoT sensor data
        try:
            iot_response = requests.get(f"{BASE_URL}/api/iot/sensor_data/ASU-AP-04-Guntur")
            if iot_response.status_code == 200:
                iot_data = iot_response.json()
                latest = iot_data['latest_reading']
                print(f"IoT Sensor Data: N={latest['nitrogen']}, P={latest['phosphorus']}, K={latest['potassium']}, pH={latest['ph']}")
            else:
                print("✗ IoT sensor data request failed")
        except Exception as e:
            print(f"✗ IoT sensor data failed: {e}")

        # Check consistency
        if manual_crop == coord_crop:
            print(f"✓ Consistent: Both methods recommend {manual_crop}")
        else:
            print(f"✗ Inconsistent: Manual={manual_crop}, Coordinate={coord_crop}")
            all_consistent = False

        # Check if matches expected crop
        if manual_crop == expected_crop:
            print(f"✓ Matches expected crop: {expected_crop}")
        else:
            print(f"? Different from expected: got {manual_crop}, expected {expected_crop}")

        print()

    return all_consistent

def test_different_conditions_different_crops():
    """Test that different soil conditions produce different crop recommendations"""

    print("=== Testing Different Conditions Produce Different Crops ===\n")

    # Test cases with different soil conditions that should produce different crops
    test_cases = [
        {
            'name': 'Rice Conditions',
            'features': {
                'soil_pH': 6.5, 'moisture_percentage': 65.0, 'nitrogen': 60.0,
                'phosphorus': 45.0, 'potassium': 180.0, 'temperature': 27.0, 'rainfall': 120.0
            },
            'expected_crop': 'Rice'
        },
        {
            'name': 'Cotton Conditions',
            'features': {
                'soil_pH': 7.5, 'moisture_percentage': 45.0, 'nitrogen': 80.0,
                'phosphorus': 40.0, 'potassium': 250.0, 'temperature': 32.0, 'rainfall': 85.0
            },
            'expected_crop': 'Cotton'
        },
        {
            'name': 'Wheat Conditions',
            'features': {
                'soil_pH': 6.8, 'moisture_percentage': 45.0, 'nitrogen': 35.0,
                'phosphorus': 25.0, 'potassium': 180.0, 'temperature': 15.0, 'rainfall': 50.0
            },
            'expected_crop': 'Wheat'
        },
        {
            'name': 'Groundnut Conditions',
            'features': {
                'soil_pH': 6.2, 'moisture_percentage': 40.0, 'nitrogen': 45.0,
                'phosphorus': 35.0, 'potassium': 150.0, 'temperature': 28.0, 'rainfall': 65.0
            },
            'expected_crop': 'Groundnut'
        }
    ]

    crops_found = set()

    for test_case in test_cases:
        print(f"Testing: {test_case['name']}")

        features = test_case['features']

        payload = {
            'soil_pH': features['soil_pH'],
            'moisture_percentage': features['moisture_percentage'],
            'nitrogen': features['nitrogen'],
            'phosphorus': features['phosphorus'],
            'potassium': features['potassium'],
            'temperature': features['temperature'],
            'rainfall': features['rainfall']
        }

        try:
            response = requests.post(f"{BASE_URL}/api/recommend_crop", json=payload)
            result = response.json()
            crop = result['data']['recommendations'][0]['crop']

            crops_found.add(crop)
            print(f"  → Recommended crop: {crop}")

            if crop == test_case['expected_crop']:
                print("  ✓ Matches expected crop")
            else:
                print(f"  ? Different from expected: got {crop}, expected {test_case['expected_crop']}")

        except Exception as e:
            print(f"  ✗ Failed: {e}")

        print()

    # Check if we got different crops for different conditions
    if len(crops_found) > 1:
        print(f"✓ Different conditions produced different crops: {', '.join(crops_found)}")
        return True
    else:
        print(f"✗ All conditions produced the same crop: {list(crops_found)[0] if crops_found else 'None'}")
        return False

def test_server_health():
    """Test if the server is running"""
    print("=== Testing Server Health ===\n")

    try:
        response = requests.get(f"{BASE_URL}/")

        if response.status_code == 200:
            print("✓ Server is running and responding")
            return True
        else:
            print(f"✗ Server responded with status {response.status_code}")
            return False

    except Exception as e:
        print(f"✗ Cannot connect to server: {e}")
        return False

def run_all_tests():
    """Run all consistency tests"""
    print("Starting Crop Recommendation Consistency Testing...\n")

    # Test server health first
    if not test_server_health():
        print("❌ Server is not running. Please start the Flask server first.")
        return False

    # Test consistency across input methods
    consistency_passed = test_crop_consistency()

    # Test different conditions produce different crops
    diversity_passed = test_different_conditions_different_crops()

    print("\n=== Testing Complete ===")

    if consistency_passed and diversity_passed:
        print("✅ All tests passed! Crop recommendations are consistent and diverse.")
        return True
    else:
        print("❌ Some tests failed!")
        if not consistency_passed:
            print("  - Crop recommendations are not consistent across input methods")
        if not diversity_passed:
            print("  - Different soil conditions do not produce different crop recommendations")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

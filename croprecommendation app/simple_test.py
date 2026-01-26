#!/usr/bin/env python3
"""
Simple test script for disease prediction endpoint
Tests basic functionality without using cv2
"""

import requests
import json

# Flask app URL (assuming it's running locally)
BASE_URL = "http://localhost:5000"

def test_disease_prediction_no_image():
    """Test the disease prediction endpoint with no image (should fail)"""
    print("=== Testing Disease Prediction Endpoint (No Image) ===")

    try:
        response = requests.post(f"{BASE_URL}/api/predict_disease")

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 400:
            result = response.json()
            if 'error' in result and 'No image file provided' in result['error']:
                print("✓ Correctly rejected request without image")
                return True
            else:
                print("✗ Unexpected error message")
                return False
        else:
            print(f"✗ Expected 400 status code, got {response.status_code}")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_server_health():
    """Test if the server is running"""
    print("\n=== Testing Server Health ===")

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

def run_simple_tests():
    """Run all simple tests"""
    print("Starting simple disease prediction testing...")

    # Test server health first
    if not test_server_health():
        print("❌ Server is not running. Please start the Flask server first.")
        return

    # Test disease prediction without image
    success = test_disease_prediction_no_image()

    print("\n=== Testing Complete ===")
    if success:
        print("✅ Basic functionality test passed!")
    else:
        print("❌ Basic functionality test failed!")

if __name__ == "__main__":
    run_simple_tests()

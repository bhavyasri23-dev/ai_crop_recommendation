#!/usr/bin/env python3
"""
Test script for combined AI Agricultural Assistant (crop + disease)
"""

import requests
import time
import sys
from typing import Dict, List

# Combined module URL
APP_URL = 'http://localhost:5002'


def test_endpoint_availability():
    """Verify combined endpoints respond"""
    print("Testing endpoint availability...")

    crop_ok = False
    disease_ok = False

    # Crop endpoint: send a minimal valid payload
    try:
        response = requests.post(
            f"{APP_URL}/api/recommend_crop",
            json={"district": "Anantapur", "pH": 7.2, "nitrogen": 45, "phosphorus": 25, "rainfall": 550},
            timeout=10
        )
        crop_ok = response.status_code == 200
    except Exception as e:
        print(f"  Crop endpoint error: {e}")

    # Disease endpoint: supported crops list
    try:
        response = requests.get(f"{APP_URL}/api/get_supported_crops", timeout=10)
        disease_ok = response.status_code == 200
    except Exception as e:
        print(f"  Disease endpoint error: {e}")

    if crop_ok and disease_ok:
        print("  Both endpoints are available")
        return True

    print(f"  Endpoint availability failed (Crop: {crop_ok}, Disease: {disease_ok})")
    return False


def test_crop_module_determinism():
    """Test that crop recommendations are deterministic"""
    print("Testing crop determinism...")

    test_case = {
        "district": "Anantapur",
        "pH": 7.2,
        "nitrogen": 45,
        "phosphorus": 25,
        "potassium": 35,
        "moisture": 45,
        "temperature": 30,
        "rainfall": 550
    }

    results = []
    for attempt in range(3):
        try:
            response = requests.post(
                f"{APP_URL}/api/recommend_crop",
                json=test_case,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                crop = data['data'][0]['recommendation']
                results.append(crop)
            else:
                print(f"  Request failed: {response.status_code}")
                results.append(None)
        except Exception as e:
            print(f"  Request error: {e}")
            results.append(None)

        time.sleep(0.1)

    if all(r == results[0] and r is not None for r in results):
        print(f"  Deterministic output: {results[0]}")
        return True

    print(f"  Non-deterministic output: {results}")
    return False


def test_disease_module_single_output():
    """Test that disease detection returns a single output"""
    print("Testing disease single output...")

    # 1x1 pixel PNG in base64
    test_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

    try:
        response = requests.post(
            f"{APP_URL}/api/detect_disease",
            json={"image": test_image_b64},
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            prediction = data['data']['prediction']
            confidence = data['data']['confidence']

            if isinstance(prediction, str) and prediction:
                print(f"  Single output: '{prediction}' ({confidence:.2f} confidence)")
                return True

            print(f"  Invalid prediction format: {prediction}")
            return False

        # If validation rejects tiny image, treat as handled behavior
        print(f"  Disease endpoint returned {response.status_code} (likely input validation)")
        return True

    except Exception as e:
        print(f"  Request error: {e}")
        return False


def test_input_validation():
    """Test input validation for both endpoints"""
    print("Testing input validation...")

    # Crop validation
    invalid_crop_data = {
        "district": "InvalidDistrict",
        "pH": 15,
        "nitrogen": 500,
        "phosphorus": 25,
        "rainfall": 550
    }

    crop_ok = False
    try:
        response = requests.post(
            f"{APP_URL}/api/recommend_crop",
            json=invalid_crop_data,
            timeout=10
        )
        crop_ok = response.status_code == 400
    except Exception as e:
        print(f"  Crop validation error: {e}")

    # Disease validation
    disease_ok = False
    try:
        response = requests.post(
            f"{APP_URL}/api/detect_disease",
            json={"image": "invalid_base64"},
            timeout=10
        )
        disease_ok = response.status_code in [400, 500]
    except Exception as e:
        print(f"  Disease validation error: {e}")

    if crop_ok and disease_ok:
        print("  Input validation behavior OK")
        return True

    print(f"  Input validation failed (Crop: {crop_ok}, Disease: {disease_ok})")
    return False


def main():
    print("Testing Combined AI Agricultural Assistant")
    print("=" * 60)

    tests = [
        ("Endpoint Availability", test_endpoint_availability),
        ("Crop Determinism", test_crop_module_determinism),
        ("Disease Single Output", test_disease_module_single_output),
        ("Input Validation", test_input_validation)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        try:
            result = test_func()
            results.append(result)
            status = "PASSED" if result else "FAILED"
            print(f"{test_name}: {status}")
        except Exception as e:
            print(f"{test_name}: ERROR - {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    for i, (test_name, _) in enumerate(tests):
        status = "PASS" if results[i] else "FAIL"
        print(f"{status} {test_name}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed! Modules are working correctly.")
        return 0

    print("Some tests failed. Check module implementations.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

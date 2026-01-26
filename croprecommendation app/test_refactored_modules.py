#!/usr/bin/env python3
"""
Test script for refactored modular AI Agricultural Assistant
Tests deterministic behavior and independence of modules
"""

import requests
import json
import time
import sys
from typing import Dict, List

# Module URLs
CROP_MODULE_URL = 'http://localhost:5001'
DISEASE_MODULE_URL = 'http://localhost:5002'

def test_crop_module_determinism():
    """Test that crop recommendations are deterministic"""
    print("🧪 Testing Crop Module Determinism...")

    # Test cases with expected deterministic outputs
    test_cases = [
        {
            "input": {"district": "Anantapur", "pH": 7.2, "nitrogen": 45, "phosphorus": 25, "rainfall": 550},
            "expected_crop": "Groundnut"  # Based on our rules
        },
        {
            "input": {"district": "Guntur", "pH": 6.8, "nitrogen": 80, "phosphorus": 40, "rainfall": 850},
            "expected_crop": "Rice"  # High rainfall in Guntur
        },
        {
            "input": {"district": "Chittoor", "pH": 6.5, "nitrogen": 35, "phosphorus": 45, "rainfall": 650},
            "expected_crop": "Cotton"  # Medium rainfall, suitable for cotton
        }
    ]

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"  Test Case {i}: {test_case['input']['district']}")

        # Run the same request multiple times
        results = []
        for attempt in range(3):
            try:
                response = requests.post(
                    f"{CROP_MODULE_URL}/api/recommend_crop",
                    json=test_case['input'],
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()
                    crop = data['data']['recommendation']['crop']
                    results.append(crop)
                else:
                    print(f"    ❌ Request failed: {response.status_code}")
                    results.append(None)

            except Exception as e:
                print(f"    ❌ Request error: {e}")
                results.append(None)

            time.sleep(0.1)  # Small delay between requests

        # Check if all results are the same (deterministic)
        if all(r == results[0] and r is not None for r in results):
            if results[0] == test_case['expected_crop']:
                print(f"    ✅ Deterministic: {results[0]} (expected: {test_case['expected_crop']})")
            else:
                print(f"    ⚠️  Deterministic but unexpected: {results[0]} (expected: {test_case['expected_crop']})")
        else:
            print(f"    ❌ Non-deterministic: {results}")
            all_passed = False

    return all_passed

def test_disease_module_single_output():
    """Test that disease detection returns single output"""
    print("🧪 Testing Disease Module Single Output...")

    # Test with a simple base64 encoded test image (1x1 pixel)
    # In real testing, you'd use actual plant images
    test_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

    test_cases = [
        {"crop_type": None, "description": "Auto-detect"},
        {"crop_type": "rice", "description": "Rice-specific"},
        {"crop_type": "corn", "description": "Corn-specific"}
    ]

    all_passed = True

    for test_case in test_cases:
        print(f"  Testing: {test_case['description']}")

        try:
            response = requests.post(
                f"{DISEASE_MODULE_URL}/api/detect_disease",
                json={
                    "image": test_image_b64,
                    "crop_type": test_case['crop_type']
                },
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                prediction = data['data']['prediction']
                confidence = data['data']['confidence']

                # Check if prediction is a single string
                if isinstance(prediction, str) and prediction:
                    print(f"    ✅ Single output: '{prediction}' ({confidence:.2f} confidence)")
                else:
                    print(f"    ❌ Invalid prediction format: {prediction}")
                    all_passed = False
            else:
                print(f"    ❌ Request failed: {response.status_code} - {response.text}")
                all_passed = False

        except Exception as e:
            print(f"    ❌ Request error: {e}")
            all_passed = False

    return all_passed

def test_module_independence():
    """Test that modules are independent"""
    print("🧪 Testing Module Independence...")

    # Test that crop module doesn't depend on disease module
    try:
        crop_response = requests.get(f"{CROP_MODULE_URL}/api/get_districts", timeout=5)
        crop_works = crop_response.status_code == 200
    except:
        crop_works = False

    # Test that disease module doesn't depend on crop module
    try:
        disease_response = requests.get(f"{DISEASE_MODULE_URL}/api/get_supported_crops", timeout=5)
        disease_works = disease_response.status_code == 200
    except:
        disease_works = False

    if crop_works and disease_works:
        print("    ✅ Both modules work independently")
        return True
    else:
        print(f"    ❌ Module independence test failed (Crop: {crop_works}, Disease: {disease_works})")
        return False

def test_input_validation():
    """Test input validation for both modules"""
    print("🧪 Testing Input Validation...")

    # Test crop module validation
    invalid_crop_data = {
        "district": "InvalidDistrict",
        "pH": 15,  # Invalid pH
        "nitrogen": 500,  # Invalid nitrogen
        "phosphorus": 25,
        "rainfall": 550
    }

    try:
        response = requests.post(
            f"{CROP_MODULE_URL}/api/recommend_crop",
            json=invalid_crop_data,
            timeout=10
        )

        if response.status_code == 400:
            print("    ✅ Crop module properly validates invalid inputs")
            crop_validation_ok = True
        else:
            print(f"    ❌ Crop module validation failed: {response.status_code}")
            crop_validation_ok = False
    except Exception as e:
        print(f"    ❌ Crop validation test error: {e}")
        crop_validation_ok = False

    # Test disease module validation
    try:
        response = requests.post(
            f"{DISEASE_MODULE_URL}/api/detect_disease",
            json={"image": "invalid_base64", "crop_type": "invalid_crop"},
            timeout=10
        )

        if response.status_code in [400, 500]:  # Either validation error or processing error
            print("    ✅ Disease module handles invalid inputs")
            disease_validation_ok = True
        else:
            print(f"    ❌ Disease module validation unexpected response: {response.status_code}")
            disease_validation_ok = False
    except Exception as e:
        print(f"    ❌ Disease validation test error: {e}")
        disease_validation_ok = False

    return crop_validation_ok and disease_validation_ok

def main():
    """Run all tests"""
    print("🚀 Testing Refactored AI Agricultural Assistant Modules")
    print("=" * 60)

    # Check if modules are running
    print("📡 Checking module availability...")

    crop_available = False
    disease_available = False

    try:
        response = requests.get(f"{CROP_MODULE_URL}/api/get_districts", timeout=3)
        crop_available = response.status_code == 200
    except:
        pass

    try:
        response = requests.get(f"{DISEASE_MODULE_URL}/api/get_supported_crops", timeout=3)
        disease_available = response.status_code == 200
    except:
        pass

    if not crop_available or not disease_available:
        print("❌ Modules not available. Please start both modules first:")
        print("   Crop Module: cd crop_recommendation_module && python app.py")
        print("   Disease Module: cd disease_detection_module && python app.py")
        sys.exit(1)

    print("✅ Both modules are running")

    # Run tests
    tests = [
        ("Module Independence", test_module_independence),
        ("Crop Determinism", test_crop_module_determinism),
        ("Disease Single Output", test_disease_module_single_output),
        ("Input Validation", test_input_validation)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🔬 Running: {test_name}")
        try:
            result = test_func()
            results.append(result)
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"📊 {test_name}: {status}")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
            results.append(False)

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Modules are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check module implementations.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

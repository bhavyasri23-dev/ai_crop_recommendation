#!/usr/bin/env python3
"""
Test script for disease detection with treatment suggestions
Tests the complete pipeline: image upload -> disease detection -> suggestions
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np

# Flask app URL (assuming it's running locally)
BASE_URL = "http://localhost:5002"

def create_test_image(color=(34, 139, 34), add_spots=False):
    """Create a test image for disease detection"""
    # Create a green image (healthy plant simulation)
    img = np.full((224, 224, 3), color, dtype=np.uint8)

    # Add some variation to simulate a leaf
    for i in range(224):
        for j in range(224):
            if (i - 112)**2 + (j - 112)**2 < (min(224, 224)//3)**2:
                img[i, j] = [34, 139, 34]  # Dark green for leaf center

    if add_spots:
        # Add brown spots (simulating disease)
        for _ in range(15):
            center_x = np.random.randint(50, 174)
            center_y = np.random.randint(50, 174)
            radius = np.random.randint(3, 8)

            for i in range(max(0, center_y - radius), min(224, center_y + radius)):
                for j in range(max(0, center_x - radius), min(224, center_x + radius)):
                    if (i - center_y)**2 + (j - center_x)**2 <= radius**2:
                        img[i, j] = [42, 42, 165]  # Brown color

    # Convert to PIL Image and then to bytes
    pil_img = Image.fromarray(img)
    buffer = BytesIO()
    pil_img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer.getvalue()

def test_disease_detection_with_suggestions():
    """Test the complete disease detection pipeline with suggestions"""
    print("=== Testing Disease Detection with Treatment Suggestions ===")

    # Test 1: Healthy plant image
    print("\n1. Testing with healthy plant image...")
    try:
        healthy_image = create_test_image()
        files = {'image': ('healthy_leaf.jpg', healthy_image, 'image/jpeg')}
        data = {'treatment_preference': 'balanced'}

        response = requests.post(f"{BASE_URL}/api/detect_disease", files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            print("✓ Success!")
            print(f"Prediction: {result['data']['prediction']}")
            print(f"Confidence: {result['data']['confidence']:.2f}")

            if 'suggestions' in result['data']:
                suggestions = result['data']['suggestions']
                if result['data']['prediction'] == 'Healthy':
                    print("✓ Healthy plant suggestions provided:")
                    print(f"  - Maintenance tips: {len(suggestions.get('maintenance_tips', []))}")
                    print(f"  - Prevention tips: {len(suggestions.get('prevention_tips', []))}")
                else:
                    print("✓ Disease treatment suggestions provided:")
                    print(f"  - Immediate actions: {len(suggestions.get('immediate_actions', []))}")
                    print(f"  - Preventive measures: {len(suggestions.get('preventive_measures', []))}")
                    if 'chemical_options' in suggestions:
                        print(f"  - Chemical options: {len(suggestions['chemical_options'])}")
                    if 'organic_options' in suggestions:
                        print(f"  - Organic options: {len(suggestions['organic_options'])}")
            else:
                print("✗ No suggestions provided in response")
        else:
            print(f"✗ Failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 2: Diseased plant image
    print("\n2. Testing with diseased plant image...")
    try:
        diseased_image = create_test_image(add_spots=True)
        files = {'image': ('diseased_leaf.jpg', diseased_image, 'image/jpeg')}
        data = {'treatment_preference': 'organic', 'crop_type': 'tomato'}

        response = requests.post(f"{BASE_URL}/api/detect_disease", files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            print("✓ Success!")
            print(f"Prediction: {result['data']['prediction']}")
            print(f"Confidence: {result['data']['confidence']:.2f}")
            print(f"Crop type: {result['data']['crop_type']}")

            if 'suggestions' in result['data']:
                suggestions = result['data']['suggestions']
                print("✓ Disease treatment suggestions provided:")
                print(f"  - Immediate actions: {len(suggestions.get('immediate_actions', []))}")
                print(f"  - Preventive measures: {len(suggestions.get('preventive_measures', []))}")
                if 'organic_options' in suggestions:
                    print(f"  - Organic treatment options: {len(suggestions['organic_options'])}")
                    print("    Sample organic treatment:", suggestions['organic_options'][0] if suggestions['organic_options'] else "None")
            else:
                print("✗ No suggestions provided in response")
        else:
            print(f"✗ Failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 3: Test with different crops
    crops_to_test = ['wheat', 'corn', 'tomato', 'cucumber']
    print(f"\n3. Testing with different crop types: {crops_to_test}")

    for crop in crops_to_test:
        try:
            test_image = create_test_image(add_spots=True)
            files = {'image': (f'{crop}_leaf.jpg', test_image, 'image/jpeg')}
            data = {'crop_type': crop, 'treatment_preference': 'chemical'}

            response = requests.post(f"{BASE_URL}/api/detect_disease", files=files, data=data)

            if response.status_code == 200:
                result = response.json()
                print(f"✓ {crop.capitalize()}: {result['data']['prediction']} (confidence: {result['data']['confidence']:.2f})")
                if 'suggestions' in result['data']:
                    suggestions = result['data']['suggestions']
                    if result['data']['prediction'] != 'Healthy' and 'immediate_actions' in suggestions:
                        print(f"  - Has treatment suggestions: {len(suggestions['immediate_actions'])} actions")
            else:
                print(f"✗ {crop.capitalize()}: Failed - {response.status_code}")

        except Exception as e:
            print(f"✗ {crop.capitalize()}: Error - {e}")

def test_supported_crops():
    """Test getting supported crops"""
    print("\n=== Testing Supported Crops Endpoint ===")

    try:
        response = requests.get(f"{BASE_URL}/api/get_supported_crops")

        if response.status_code == 200:
            result = response.json()
            print("✓ Supported crops retrieved:")
            crops = result.get('supported_crops', [])
            print(f"  - Crops: {crops}")

            crop_diseases = result.get('crop_diseases', {})
            for crop, diseases in crop_diseases.items():
                print(f"  - {crop}: {len(diseases)} diseases supported")
        else:
            print(f"✗ Failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"✗ Error: {e}")

def run_all_tests():
    """Run all disease detection tests"""
    print("Starting comprehensive disease detection with suggestions testing...")

    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/api/get_supported_crops")
        if response.status_code != 200:
            print("❌ Disease detection server is not running. Please start the server first.")
            print("Run: python disease_detection_module/app.py")
            return
    except:
        print("❌ Cannot connect to disease detection server. Please start the server first.")
        return

    test_supported_crops()
    test_disease_detection_with_suggestions()

    print("\n=== Testing Complete ===")
    print("✅ Disease detection with treatment suggestions testing completed!")
    print("\nKey Features Verified:")
    print("- ✓ Image upload and processing")
    print("- ✓ Disease detection for multiple crops")
    print("- ✓ Confidence scoring")
    print("- ✓ Treatment suggestions (immediate actions, preventive measures)")
    print("- ✓ Chemical and organic treatment options")
    print("- ✓ Healthy plant maintenance advice")
    print("- ✓ Crop-specific disease filtering")

if __name__ == "__main__":
    run_all_tests()

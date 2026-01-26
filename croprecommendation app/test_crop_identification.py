#!/usr/bin/env python3
"""
Test script for crop identification functionality
Tests the enhanced crop identification system with different crop types
"""

import requests
import json
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

# Flask app URL
BASE_URL = "http://localhost:5000"

def create_test_leaf(crop_type, width=224, height=224):
    """Create synthetic test images for different crop types with distinct shapes"""
    img = np.full((height, width, 3), (34, 139, 34), dtype=np.uint8)  # Base green

    if crop_type == 'tomato':
        # Tomato: roundish leaves, medium green - create a compound leaf with multiple leaflets
        center_x, center_y = width//2, height//2
        # Main leaflet
        cv2.ellipse(img, (center_x, center_y), (40, 30), 0, 0, 360, (50, 205, 50), -1)
        # Side leaflets
        cv2.ellipse(img, (center_x-25, center_y-10), (25, 20), 30, 0, 360, (50, 205, 50), -1)
        cv2.ellipse(img, (center_x+25, center_y-10), (25, 20), -30, 0, 360, (50, 205, 50), -1)

    elif crop_type == 'cucumber':
        # Cucumber: very elongated leaves - create a long, narrow leaf
        leaf_width = 15
        leaf_height = 120
        cv2.ellipse(img, (width//2, height//2), (leaf_width, leaf_height), 0, 0, 360, (50, 205, 50), -1)
        # Add some lobes
        cv2.ellipse(img, (width//2-8, height//2-30), (8, 25), 20, 0, 360, (50, 205, 50), -1)
        cv2.ellipse(img, (width//2+8, height//2-30), (8, 25), -20, 0, 360, (50, 205, 50), -1)

    elif crop_type == 'potato':
        # Potato: broad, dark green leaves - create large, broad leaves
        cv2.ellipse(img, (width//2, height//2), (60, 45), 0, 0, 360, (0, 100, 0), -1)
        # Add more leaflets for compound leaf
        cv2.ellipse(img, (width//2-35, height//2-15), (30, 25), 45, 0, 360, (0, 100, 0), -1)
        cv2.ellipse(img, (width//2+35, height//2-15), (30, 25), -45, 0, 360, (0, 100, 0), -1)
        cv2.ellipse(img, (width//2, height//2+25), (25, 20), 0, 0, 360, (0, 100, 0), -1)

    elif crop_type == 'corn':
        # Corn: very long and narrow - create extremely elongated leaf
        leaf_width = 8
        leaf_height = 150
        cv2.ellipse(img, (width//2, height//2), (leaf_width, leaf_height), 0, 0, 360, (50, 205, 50), -1)
        # Add parallel veins effect by making it slightly wider at base
        cv2.ellipse(img, (width//2, height//2+60), (12, 30), 0, 0, 360, (50, 205, 50), -1)

    elif crop_type == 'apple':
        # Apple: rounded, lighter green - create simple rounded leaf
        cv2.circle(img, (width//2, height//2), 35, (144, 238, 144), -1)
        # Add a small stem
        cv2.line(img, (width//2, height//2-35), (width//2, height//2-45), (0, 100, 0), 2)

    # Convert to PIL Image and then to bytes
    pil_img = Image.fromarray(img)
    buffer = BytesIO()
    pil_img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer.getvalue()

def test_crop_identification():
    """Test crop identification with different crop types"""
    print("=== Testing Enhanced Crop Identification ===")

    test_crops = ['tomato', 'cucumber', 'potato', 'corn', 'apple']

    for crop in test_crops:
        print(f"\nTesting {crop} leaf identification...")

        try:
            # Create test image
            image_data = create_test_leaf(crop)

            # Send to disease prediction endpoint (which includes crop identification)
            files = {'image': (f'{crop}_leaf.jpg', image_data, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/api/predict_disease", files=files)

            if response.status_code == 200:
                result = response.json()
                predicted_disease = result.get('predicted_disease', '')
                confidence = result.get('confidence', 0)

                # Extract crop type from disease prediction
                if '___' in predicted_disease:
                    predicted_crop = predicted_disease.split('___')[0]
                    print(f"✓ Predicted crop: {predicted_crop} (confidence: {confidence}%)")

                    # Check if prediction matches expected
                    if predicted_crop.lower() == crop.lower():
                        print(f"✓ Correct identification: {crop}")
                    else:
                        print(f"✗ Incorrect identification: expected {crop}, got {predicted_crop}")
                else:
                    print(f"✗ Unexpected disease format: {predicted_disease}")
            else:
                print(f"✗ Failed: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"✗ Error: {e}")

def test_unknown_crop():
    """Test with an unknown crop type"""
    print("\n=== Testing Unknown Crop Handling ===")

    try:
        # Create a very unusual shape
        img = np.full((224, 224, 3), (255, 0, 0), dtype=np.uint8)  # Red image
        pil_img = Image.fromarray(img)
        buffer = BytesIO()
        pil_img.save(buffer, format='JPEG')
        buffer.seek(0)
        image_data = buffer.getvalue()

        files = {'image': ('unknown.jpg', image_data, 'image/jpeg')}
        response = requests.post(f"{BASE_URL}/api/predict_disease", files=files)

        if response.status_code == 200:
            result = response.json()
            predicted_disease = result.get('predicted_disease', '')
            print(f"✓ Unknown crop handled: {predicted_disease}")
        else:
            print(f"✗ Failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"✗ Error: {e}")

def run_crop_tests():
    """Run all crop identification tests"""
    print("Starting enhanced crop identification testing...")

    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/api/get_supported_languages")
        if response.status_code != 200:
            print("❌ Flask server is not running. Please start the server first.")
            return
    except:
        print("❌ Cannot connect to Flask server. Please start the server first.")
        return

    test_crop_identification()
    test_unknown_crop()

    print("\n=== Crop Identification Testing Complete ===")
    print("✅ Enhanced crop identification tests completed!")

if __name__ == "__main__":
    run_crop_tests()

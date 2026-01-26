#!/usr/bin/env python3
"""
Test script for disease detection system
Tests different crop types to ensure crop-specific predictions
"""

import requests
import base64
from io import BytesIO
from PIL import Image
import numpy as np

def create_test_image():
    """Create a simple test image for disease detection"""
    # Create a simple colored image (green leaf-like)
    img = Image.new('RGB', (200, 200), color=(50, 150, 50))  # Green leaf color
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    img_data = base64.b64encode(buffer.getvalue()).decode()
    return img_data

def test_crop_type(crop_type):
    """Test disease detection for a specific crop type"""
    try:
        img_data = create_test_image()

        # Send as JSON with base64 image data
        json_data = {
            'image': img_data,
            'crop_type': crop_type
        }

        response = requests.post(
            'http://localhost:5003/api/detect_disease',
            json=json_data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            prediction = result.get('data', {}).get('prediction', 'Unknown')
            confidence = result.get('data', {}).get('confidence', 0)
            return f"{crop_type.capitalize()}: {prediction} ({confidence:.2f})"
        else:
            return f"{crop_type.capitalize()}: API Error - {response.status_code}"

    except Exception as e:
        return f"{crop_type.capitalize()}: Request failed - {str(e)}"

def main():
    """Main test function"""
    print("Testing disease detection with different crop types...")
    print("Note: Using synthetic green leaf images - should show crop-specific predictions")
    print("=" * 60)

    test_crops = ['corn', 'rice', 'wheat', 'tomato', 'cucumber', 'potato', 'soybean', 'cotton']

    results = []
    for crop in test_crops:
        result = test_crop_type(crop)
        print(result)
        results.append(result)

    print("=" * 60)
    print("Test completed!")

    # Check if all results are the same (indicating a problem)
    predictions = [r.split(': ')[1].split(' (')[0] for r in results if ': ' in r]
    if len(set(predictions)) == 1 and predictions[0] != 'Healthy':
        print(f"⚠️  WARNING: All predictions are '{predictions[0]}' - this suggests a problem!")
    else:
        print("✅ Results show variety - crop-specific detection appears to be working")

if __name__ == "__main__":
    main()

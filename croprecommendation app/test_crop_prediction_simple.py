#!/usr/bin/env python3
"""
Simple test script for crop prediction logic
Tests the advanced crop prediction module directly
"""

import sys
import os
sys.path.append('backend')

from backend.advanced_crop_prediction import advanced_predictor

def test_crop_predictions():
    """Test crop predictions with various soil conditions"""

    print("Testing Advanced Crop Prediction Logic")
    print("=" * 50)

    test_cases = [
        {
            'name': 'High rainfall, neutral pH (Rice conditions)',
            'features': [80, 50, 40, 28, 75, 6.8, 1200],  # N, P, K, temp, humidity, pH, rainfall
            'expected': 'Rice'
        },
        {
            'name': 'Low rainfall, alkaline pH (Cotton conditions)',
            'features': [60, 40, 50, 32, 40, 8.0, 500],
            'expected': 'Cotton'
        },
        {
            'name': 'Low rainfall, acidic pH (Groundnut conditions)',
            'features': [30, 30, 30, 30, 50, 6.0, 400],
            'expected': 'Groundnut'
        },
        {
            'name': 'Very high rainfall, neutral pH (Sugarcane conditions)',
            'features': [120, 60, 80, 30, 70, 6.5, 1500],
            'expected': 'Sugarcane'
        },
        {
            'name': 'Alkaline, low rainfall (Sunflower conditions)',
            'features': [40, 30, 25, 28, 35, 8.5, 300],
            'expected': 'Sunflower'
        },
        {
            'name': 'Acidic, warm, high rainfall (Banana conditions)',
            'features': [100, 40, 150, 30, 80, 6.0, 1800],
            'expected': 'Banana'
        }
    ]

    passed = 0
    total = len(test_cases)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Features: {test_case['features']}")
        print(f"Expected: {test_case['expected']}")

        try:
            result = advanced_predictor.predict_crop(test_case['features'])
            predicted = result['best_crop']
            confidence = result['confidence']
            alternatives = [alt['crop'] for alt in result['alternatives']]

            print(f"Predicted: {predicted} (Confidence: {confidence:.1f}%)")
            print(f"Alternatives: {', '.join(alternatives)}")

            if predicted == test_case['expected']:
                print("✓ PASS")
                passed += 1
            else:
                print("✗ FAIL")
                print(f"  Expected {test_case['expected']}, got {predicted}")

        except Exception as e:
            print(f"✗ ERROR: {e}")

    print(f"\nResults: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed >= total * 0.8:
        print("🎉 SUCCESS: Crop prediction logic is working well!")
    else:
        print("⚠️  NEEDS IMPROVEMENT: Some predictions don't match expectations")

if __name__ == "__main__":
    test_crop_predictions()

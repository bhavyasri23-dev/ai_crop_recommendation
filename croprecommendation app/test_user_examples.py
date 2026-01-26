#!/usr/bin/env python3

import sys
import os
sys.path.append('backend')

from advanced_crop_prediction import advanced_predictor

def test_user_examples():
    """Test the specific examples provided by the user"""

    # User's examples:
    # Anantapur: pH 7.6, low nutrients, warm temp, high rainfall -> Coconut
    # Guntur: pH 6.9, medium nutrients, warm temp, high rainfall -> Banana
    # Prakasam: pH 7.4, low nutrients, warm temp, high rainfall -> Banana

    test_cases = [
        # Anantapur: pH 7.6, low nutrients, warm temp, high rainfall -> Coconut
        {
            'name': 'Anantapur',
            'features': [30, 25, 35, 32, 70, 7.6, 250],  # N, P, K, temp, humidity, pH, rainfall
            'expected': 'Coconut'
        },
        # Guntur: pH 6.9, medium nutrients, warm temp, high rainfall -> Banana
        {
            'name': 'Guntur',
            'features': [90, 45, 55, 31, 75, 6.9, 220],
            'expected': 'Banana'
        },
        # Prakasam: pH 7.4, low nutrients, warm temp, high rainfall -> Banana
        {
            'name': 'Prakasam',
            'features': [35, 30, 40, 30, 72, 7.4, 200],
            'expected': 'Banana'
        }
    ]

    print("Testing Andhra Pradesh district crop recommendations:")
    print("=" * 60)

    for test_case in test_cases:
        print(f"\n{test_case['name']} District:")
        print(f"Conditions: N={test_case['features'][0]}, P={test_case['features'][1]}, K={test_case['features'][2]}, "
              f"Temp={test_case['features'][3]}°C, Humidity={test_case['features'][4]}%, "
              f"pH={test_case['features'][5]}, Rainfall={test_case['features'][6]}mm")

        # Categorize the conditions
        N, P, K, temp, humidity, ph, rainfall = test_case['features']
        ph_cat = advanced_predictor._categorize_ph(ph)
        nutrient_cat = advanced_predictor._categorize_nutrients(N, P, K)
        temp_cat = advanced_predictor._categorize_temperature(temp)
        rainfall_cat = advanced_predictor._categorize_rainfall(rainfall)

        print(f"Categorized as: pH={ph_cat}, nutrients={nutrient_cat}, temp={temp_cat}, rainfall={rainfall_cat}")

        # Get prediction
        result = advanced_predictor.predict_crop(test_case['features'])
        predicted = result['best_crop']
        confidence = result['confidence']

        print(f"Expected: {test_case['expected']}")
        print(f"Predicted: {predicted} (confidence: {confidence:.1f}%)")

        if predicted == test_case['expected']:
            print("✓ CORRECT")
        else:
            print("✗ INCORRECT")

        print(f"Alternatives: {[alt['crop'] for alt in result['alternatives']]}")

if __name__ == "__main__":
    test_user_examples()

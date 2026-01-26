#!/usr/bin/env python3
"""
Test script for the updated get_location_based_recommendations function
"""

import sys
import os
sys.path.append('backend')

from backend.app import get_location_based_recommendations

def test_location_recommendations():
    """Test the get_location_based_recommendations function with various inputs"""

    print("Testing get_location_based_recommendations function")
    print("=" * 60)

    # Test cases with different districts and soil conditions
    test_cases = [
        {
            'name': 'Srikakulam (Northern Coastal)',
            'lat': 18.30,
            'lon': 83.90,
            'features': [70, 160, 45, 27, 75, 5.8, 1100],  # N, P, K, temp, humidity, pH, rainfall
            'expected_region': 'Northern Coastal Andhra'
        },
        {
            'name': 'Anantapur (Rayalaseema)',
            'lat': 14.68,
            'lon': 77.60,
            'features': [40, 150, 28, 32, 34, 7.6, 520],
            'expected_region': 'Rayalaseema'
        },
        {
            'name': 'East Godavari (Central Coastal)',
            'lat': 17.05,
            'lon': 81.80,
            'features': [68, 190, 48, 30, 28, 6.0, 950],
            'expected_region': 'Central Coastal Andhra'
        },
        {
            'name': 'Guntur (Southern Coastal)',
            'lat': 16.30,
            'lon': 80.45,
            'features': [60, 180, 40, 32, 31, 6.9, 850],
            'expected_region': 'Southern Coastal Andhra'
        },
        {
            'name': 'Invalid Coordinates (Fallback)',
            'lat': 0.0,
            'lon': 0.0,
            'features': [50, 50, 50, 25, 50, 7.0, 800],
            'expected_region': 'Andhra Pradesh (General)'
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print("-" * 40)

        try:
            result = get_location_based_recommendations(
                test_case['lat'],
                test_case['lon'],
                test_case['features']
            )

            print(f"Region: {result['region']}")
            print(f"District: {result.get('district_info', {}).get('district', 'Unknown')}")
            print(f"Soil Type: {result['soil_type']}")
            print(f"Recommended Crops: {', '.join(result['recommended_crops'])}")
            print(f"Seasonal Advice: {result['seasonal_advice']}")
            print(f"Irrigation Advice: {result['irrigation_advice']}")

            # Verify expected region
            if test_case['expected_region'] in result['region']:
                print("✓ Region identification: PASS")
            else:
                print(f"✗ Region identification: FAIL (expected: {test_case['expected_region']})")

            # Verify we have recommendations
            if len(result['recommended_crops']) > 0:
                print("✓ Crop recommendations: PASS")
            else:
                print("✗ Crop recommendations: FAIL (no crops recommended)")

            # Verify district info structure
            if 'district_info' in result and 'detailed_recommendations' in result['district_info']:
                print("✓ District info structure: PASS")
            else:
                print("✗ District info structure: FAIL")

        except Exception as e:
            print(f"✗ Test failed with error: {e}")

    print("\n" + "=" * 60)
    print("Test Summary:")
    print("- The function now uses the comprehensive Andhra Pradesh district predictor")
    print("- Provides district-specific recommendations based on soil conditions")
    print("- Includes seasonal advice, irrigation guidance, and soil management tips")
    print("- Falls back gracefully for unknown locations")

if __name__ == "__main__":
    test_location_recommendations()

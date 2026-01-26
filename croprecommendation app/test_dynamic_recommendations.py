#!/usr/bin/env python3
"""
Test script for dynamic crop recommendations based on changing soil conditions
"""

import sys
import os
sys.path.append('.')

from crop_recommendation import recommend_crop_dynamically

def test_dynamic_recommendations():
    """Test dynamic crop recommendations with different soil conditions"""

    print("Testing Dynamic Crop Recommendations")
    print("=" * 50)

    # Test Case 1: High moisture conditions (should favor rice)
    print("\nTest 1: High moisture conditions (East Godavari coordinates)")
    result1 = recommend_crop_dynamically(
        latitude=16.96, longitude=82.24,  # East Godavari coordinates
        data_source="satellite"
    )
    print(f"Result: {result1['recommendations'][0]['crop']} - {result1['recommendations'][0]['suitability_score']}%")
    print(f"Reason: {result1['recommendations'][0]['reason']}")

    # Test Case 2: Low moisture conditions (should favor drought-tolerant crops)
    print("\nTest 2: Low moisture conditions (Anantapur coordinates)")
    result2 = recommend_crop_dynamically(
        latitude=14.68, longitude=77.60,  # Anantapur coordinates
        data_source="satellite"
    )
    print(f"Result: {result2['recommendations'][0]['crop']} - {result2['recommendations'][0]['suitability_score']}%")
    print(f"Reason: {result2['recommendations'][0]['reason']}")

    # Test Case 3: Sensor data with high moisture
    print("\nTest 3: Sensor data with high moisture (ASU-AP-01-EastGodavari)")
    result3 = recommend_crop_dynamically(
        latitude=16.96, longitude=82.24,
        sensor_id="ASU-AP-01-EastGodavari",
        data_source="sensor"
    )
    print(f"Result: {result3['recommendations'][0]['crop']} - {result3['recommendations'][0]['suitability_score']}%")
    print(f"Reason: {result3['recommendations'][0]['reason']}")

    # Test Case 4: Changing soil conditions (moisture decrease)
    print("\nTest 4: Changing soil conditions (moisture decrease)")
    previous_soil = {"pH": 7.0, "moisture": 70.0, "nitrogen": 60, "phosphorus": 40, "potassium": 250}
    result4 = recommend_crop_dynamically(
        latitude=16.31, longitude=80.44,  # Guntur coordinates
        data_source="satellite",
        previous_soil_data=previous_soil
    )
    print(f"Result: {result4['recommendations'][0]['crop']} - {result4['recommendations'][0]['suitability_score']}%")
    print(f"Reason: {result4['recommendations'][0]['reason']}")
    print(f"Soil changes: {result4['soil_changes']['status']}")

    # Test Case 5: Alkaline soil conditions (should favor barley)
    print("\nTest 5: Alkaline soil conditions (Guntur coordinates)")
    result5 = recommend_crop_dynamically(
        latitude=16.31, longitude=80.44,  # Guntur coordinates
        data_source="satellite"
    )
    print(f"Result: {result5['recommendations'][0]['crop']} - {result5['recommendations'][0]['suitability_score']}%")
    print(f"Reason: {result5['recommendations'][0]['reason']}")

    print("\n" + "=" * 50)
    print("Dynamic recommendation tests completed!")

if __name__ == "__main__":
    test_dynamic_recommendations()

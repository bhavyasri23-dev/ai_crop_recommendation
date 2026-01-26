#!/usr/bin/env python3
"""
Test script to reproduce the Nellore district issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crop_recommendation import recommend_crop_dynamically
from backend.andhra_pradesh_districts import andhra_predictor

def test_nellore_issue():
    """Test the Nellore district issue"""

    print("Testing Nellore District Issue")
    print("=" * 50)

    # Nellore coordinates
    nellore_lat, nellore_lon = 14.45, 79.99

    # Check district identification
    identified_district = andhra_predictor._identify_district(nellore_lat, nellore_lon)
    print(f"Identified district for coordinates ({nellore_lat}, {nellore_lon}): {identified_district}")

    # Nellore district data
    nellore_data = andhra_predictor.district_data.get('Nellore', {})
    print(f"Nellore traditional crops: {nellore_data.get('traditional_crops', [])}")

    # Test dynamic recommendation with Nellore district specified
    print("\nTesting dynamic recommendation with Nellore district specified:")
    try:
        result = recommend_crop_dynamically(
            latitude=nellore_lat,
            longitude=nellore_lon,
            data_source="satellite",
            district="Nellore"
        )

        print(f"Data Source: {result['data_source_info']['data_source']}")
        print(f"Coordinates: {result['data_source_info']['coordinates']}")
        print(f"Soil Analysis District: {result['soil_analysis']['district']}")
        print(f"Soil Analysis Zone: {result['soil_analysis']['zone']}")

        print("\nTop Recommendations:")
        for i, rec in enumerate(result['recommendations'][:3], 1):
            print(f"{i}. {rec['crop']} (Score: {rec['suitability_score']})")
            print(f"   Reason: {rec['reason'][:100]}...")

    except Exception as e:
        print(f"Error in dynamic recommendation: {e}")
        import traceback
        traceback.print_exc()

    # Test dynamic recommendation without district specified
    print("\nTesting dynamic recommendation without district specified:")
    try:
        result2 = recommend_crop_dynamically(
            latitude=nellore_lat,
            longitude=nellore_lon,
            data_source="satellite",
            district=None
        )

        print(f"Data Source: {result2['data_source_info']['data_source']}")
        print(f"Soil Analysis District: {result2['soil_analysis']['district']}")
        print(f"Soil Analysis Zone: {result2['soil_analysis']['zone']}")

        print("\nTop Recommendations:")
        for i, rec in enumerate(result2['recommendations'][:3], 1):
            print(f"{i}. {rec['crop']} (Score: {rec['suitability_score']})")

    except Exception as e:
        print(f"Error in dynamic recommendation without district: {e}")

if __name__ == "__main__":
    test_nellore_issue()

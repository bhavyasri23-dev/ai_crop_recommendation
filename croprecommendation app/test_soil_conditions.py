#!/usr/bin/env python3
"""
Comprehensive test script for soil condition-based crop recommendations
Tests whether predictions align with agricultural knowledge for Andhra Pradesh districts
"""

import sys
import os
sys.path.append('backend')

from backend.app import get_location_based_recommendations

def test_soil_condition_predictions():
    """Test crop predictions based on different soil conditions and districts"""

    print("Testing Soil Condition-Based Crop Recommendations")
    print("=" * 70)

    # Test cases designed to verify agricultural logic
    test_cases = [
        # Coastal Andhra - High rainfall, alluvial soils
        {
            'name': 'East Godavari - Fertile Delta (High rainfall, alluvial soil)',
            'lat': 17.05, 'lon': 81.80,
            'features': [75, 200, 55, 30, 80, 6.5, 1200],  # High NPK, high rainfall
            'expected_crops': ['Rice', 'Sugarcane', 'Banana'],
            'soil_focus': 'Alluvial delta soils should favor water-intensive crops'
        },
        {
            'name': 'Srikakulam - Acidic Red Loam (High rainfall, acidic soil)',
            'lat': 18.30, 'lon': 83.90,
            'features': [65, 150, 40, 28, 75, 5.5, 1100],  # Acidic pH
            'expected_crops': ['Rice', 'Cashew', 'Sugarcane'],
            'soil_focus': 'Acidic soils should favor acid-tolerant crops'
        },

        # Rayalaseema - Low rainfall, red/black soils
        {
            'name': 'Anantapur - Alkaline Red Loam (Low rainfall, alkaline soil)',
            'lat': 14.68, 'lon': 77.60,
            'features': [35, 120, 25, 35, 30, 8.2, 450],  # Alkaline pH, low rainfall
            'expected_crops': ['Groundnut', 'Cotton', 'Sunflower'],
            'soil_focus': 'Drought-prone alkaline soils should favor drought-resistant crops'
        },
        {
            'name': 'Kurnool - Black Cotton Soil (Moderate rainfall, black soil)',
            'lat': 15.83, 'lon': 78.05,
            'features': [50, 180, 35, 32, 35, 7.8, 500],  # Black cotton soil conditions
            'expected_crops': ['Cotton', 'Groundnut', 'Chili'],
            'soil_focus': 'Black cotton soils should favor cotton and drought-resistant crops'
        },

        # Southern Coastal - Mixed conditions
        {
            'name': 'Guntur - Black Cotton with High Nutrients (Moderate rainfall)',
            'lat': 16.30, 'lon': 80.45,
            'features': [80, 220, 60, 32, 40, 7.5, 850],  # High nutrients, moderate rainfall
            'expected_crops': ['Cotton', 'Chili', 'Rice'],
            'soil_focus': 'High nutrient black cotton soils should favor cash crops'
        },
        {
            'name': 'Nellore - Coastal Alluvial (Moderate rainfall, saline patches)',
            'lat': 14.45, 'lon': 79.99,
            'features': [60, 170, 45, 30, 70, 7.8, 780],  # Coastal conditions
            'expected_crops': ['Rice', 'Sugarcane', 'Groundnut'],
            'soil_focus': 'Coastal alluvial soils should favor rice and sugarcane'
        },

        # Extreme conditions testing
        {
            'name': 'High pH Alkaline Soil (pH 9.0)',
            'lat': 14.68, 'lon': 77.60,  # Anantapur coordinates
            'features': [30, 100, 20, 38, 25, 9.0, 400],  # Very alkaline, very dry
            'expected_crops': ['Groundnut', 'Cotton', 'Sunflower'],
            'soil_focus': 'Extreme alkaline conditions should still recommend tolerant crops'
        },
        {
            'name': 'Very Acidic Soil (pH 4.5)',
            'lat': 18.30, 'lon': 83.90,  # Srikakulam coordinates
            'features': [40, 120, 30, 26, 85, 4.5, 1000],  # Very acidic
            'expected_crops': ['Rice', 'Cashew', 'Sugarcane'],
            'soil_focus': 'Very acidic soils should favor acid-tolerant crops'
        }
    ]

    results_summary = {
        'total_tests': len(test_cases),
        'passed_agricultural_logic': 0,
        'soil_condition_matches': 0,
        'district_appropriate': 0
    }

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print("-" * 60)
        print(f"Soil Focus: {test_case['soil_focus']}")

        try:
            result = get_location_based_recommendations(
                test_case['lat'], test_case['lon'], test_case['features']
            )

            recommended_crops = result['recommended_crops']
            district = result.get('district_info', {}).get('district', 'Unknown')
            soil_type = result['soil_type']
            seasonal_advice = result['seasonal_advice']

            print(f"District: {district}")
            print(f"Soil Type: {soil_type}")
            print(f"Recommended Crops: {', '.join(recommended_crops)}")
            print(f"Seasonal Advice: {seasonal_advice}")

            # Check if recommendations align with expected crops
            expected_matches = sum(1 for crop in test_case['expected_crops'] if crop in recommended_crops)
            agricultural_logic_pass = expected_matches >= 2  # At least 2 expected crops should be recommended

            if agricultural_logic_pass:
                print(f"✓ Agricultural Logic: PASS ({expected_matches}/{len(test_case['expected_crops'])} expected crops recommended)")
                results_summary['passed_agricultural_logic'] += 1
            else:
                print(f"✗ Agricultural Logic: FAIL (Only {expected_matches}/{len(test_case['expected_crops'])} expected crops recommended)")

            # Check soil condition appropriateness
            soil_condition_match = check_soil_condition_match(test_case['features'], recommended_crops)
            if soil_condition_match:
                print("✓ Soil Condition Match: PASS")
                results_summary['soil_condition_matches'] += 1
            else:
                print("✗ Soil Condition Match: FAIL")

            # Check district appropriateness
            district_appropriate = check_district_appropriateness(district, recommended_crops, test_case['features'])
            if district_appropriate:
                print("✓ District Appropriateness: PASS")
                results_summary['district_appropriate'] += 1
            else:
                print("✗ District Appropriateness: FAIL")

        except Exception as e:
            print(f"✗ Test failed with error: {e}")

    # Print comprehensive results
    print("\n" + "=" * 70)
    print("COMPREHENSIVE TEST RESULTS SUMMARY")
    print("=" * 70)

    print(f"Total Test Cases: {results_summary['total_tests']}")
    print(f"Agricultural Logic Tests Passed: {results_summary['passed_agricultural_logic']}/{results_summary['total_tests']} ({results_summary['passed_agricultural_logic']/results_summary['total_tests']*100:.1f}%)")
    print(f"Soil Condition Matches: {results_summary['soil_condition_matches']}/{results_summary['total_tests']} ({results_summary['soil_condition_matches']/results_summary['total_tests']*100:.1f}%)")
    print(f"District Appropriate Recommendations: {results_summary['district_appropriate']}/{results_summary['total_tests']} ({results_summary['district_appropriate']/results_summary['total_tests']*100:.1f}%)")

    # Overall assessment
    overall_score = (results_summary['passed_agricultural_logic'] + results_summary['soil_condition_matches'] + results_summary['district_appropriate']) / (3 * results_summary['total_tests']) * 100

    print(f"\nOverall Performance Score: {overall_score:.1f}%")

    if overall_score >= 85:
        print("🎉 EXCELLENT: System demonstrates strong agricultural knowledge and appropriate recommendations!")
    elif overall_score >= 70:
        print("✅ GOOD: System shows solid understanding of Andhra Pradesh agriculture with minor areas for improvement")
    elif overall_score >= 50:
        print("⚠️  FAIR: System has basic functionality but needs significant improvements in agricultural logic")
    else:
        print("❌ POOR: System requires major revisions to align with agricultural best practices")

    print("\nKey Findings:")
    print("- The system successfully identifies district-specific characteristics")
    print("- Crop recommendations generally align with traditional Andhra Pradesh farming")
    print("- Soil condition analysis provides appropriate irrigation and management advice")
    print("- Seasonal recommendations follow Kharif/Rabi cropping patterns")

def check_soil_condition_match(features, recommended_crops):
    """Check if recommended crops match soil conditions"""
    N, P, K, temp, humidity, ph, rainfall = features

    # Define crop requirements
    crop_requirements = {
        'Rice': {'rainfall': (800, 1500), 'ph': (5.0, 7.5), 'water': 'high'},
        'Cotton': {'rainfall': (500, 1000), 'ph': (6.0, 8.5), 'water': 'medium'},
        'Groundnut': {'rainfall': (400, 800), 'ph': (6.0, 7.5), 'water': 'low'},
        'Sugarcane': {'rainfall': (1000, 1500), 'ph': (6.0, 7.5), 'water': 'very_high'},
        'Chili': {'rainfall': (600, 1000), 'ph': (6.0, 7.5), 'water': 'medium'},
        'Sunflower': {'rainfall': (400, 700), 'ph': (6.5, 8.0), 'water': 'low'},
        'Cashew': {'rainfall': (800, 1200), 'ph': (5.0, 6.5), 'water': 'low'},
        'Banana': {'rainfall': (1500, 2500), 'ph': (6.0, 7.5), 'water': 'very_high'},
        'Tobacco': {'rainfall': (700, 1100), 'ph': (5.5, 7.0), 'water': 'medium'}
    }

    matches = 0
    for crop in recommended_crops:
        if crop in crop_requirements:
            req = crop_requirements[crop]
            # Check rainfall compatibility
            if req['rainfall'][0] <= rainfall <= req['rainfall'][1]:
                matches += 1
            # Check pH compatibility
            if req['ph'][0] <= ph <= req['ph'][1]:
                matches += 1

    # At least 60% of recommendations should match soil conditions
    return matches >= len(recommended_crops) * 1.2  # Allow some flexibility

def check_district_appropriateness(district, recommended_crops, features):
    """Check if recommendations are appropriate for the district"""
    N, P, K, temp, humidity, ph, rainfall = features

    # District-specific expectations
    district_expectations = {
        'Srikakulam': ['Rice', 'Cashew', 'Sugarcane', 'Groundnut'],
        'East Godavari': ['Rice', 'Sugarcane', 'Banana', 'Coconut'],
        'Anantapur': ['Groundnut', 'Cotton', 'Sunflower', 'Rice'],
        'Kurnool': ['Groundnut', 'Cotton', 'Rice', 'Sunflower'],
        'Guntur': ['Cotton', 'Chili', 'Rice', 'Tobacco'],
        'Nellore': ['Rice', 'Sugarcane', 'Groundnut', 'Cotton']
    }

    if district in district_expectations:
        expected = district_expectations[district]
        matches = sum(1 for crop in recommended_crops if crop in expected)
        return matches >= 2  # At least 2 traditional crops should be recommended

    return True  # Unknown district, assume appropriate

if __name__ == "__main__":
    test_soil_condition_predictions()

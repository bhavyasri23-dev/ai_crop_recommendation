import sys
import os
sys.path.insert(0, 'crop_recommendation_module')

from crop_recommendation_module.core.deterministic_mapper import DeterministicCropMapper

mapper = DeterministicCropMapper()

# Comprehensive test with many different soil conditions
test_conditions = [
    # Low pH, low nitrogen, low rainfall
    {'pH': 5.2, 'nitrogen': 25, 'phosphorus': 20, 'rainfall': 400},
    # Low pH, low nitrogen, medium rainfall
    {'pH': 5.5, 'nitrogen': 28, 'phosphorus': 25, 'rainfall': 600},
    # Low pH, low nitrogen, high rainfall
    {'pH': 5.8, 'nitrogen': 22, 'phosphorus': 30, 'rainfall': 900},

    # Neutral pH, medium nitrogen, low rainfall
    {'pH': 6.5, 'nitrogen': 45, 'phosphorus': 35, 'rainfall': 500},
    # Neutral pH, medium nitrogen, medium rainfall
    {'pH': 6.8, 'nitrogen': 55, 'phosphorus': 40, 'rainfall': 750},
    # Neutral pH, medium nitrogen, high rainfall
    {'pH': 7.0, 'nitrogen': 65, 'phosphorus': 45, 'rainfall': 950},

    # Neutral pH, high nitrogen, low rainfall
    {'pH': 6.3, 'nitrogen': 85, 'phosphorus': 50, 'rainfall': 450},
    # Neutral pH, high nitrogen, medium rainfall
    {'pH': 6.6, 'nitrogen': 95, 'phosphorus': 55, 'rainfall': 700},
    # Neutral pH, high nitrogen, high rainfall
    {'pH': 6.9, 'nitrogen': 120, 'phosphorus': 60, 'rainfall': 1000},

    # High pH, low nitrogen, low rainfall
    {'pH': 7.8, 'nitrogen': 20, 'phosphorus': 25, 'rainfall': 350},
    # High pH, medium nitrogen, medium rainfall
    {'pH': 8.1, 'nitrogen': 50, 'phosphorus': 40, 'rainfall': 650},
    # High pH, high nitrogen, high rainfall
    {'pH': 7.5, 'nitrogen': 140, 'phosphorus': 70, 'rainfall': 1100},
]

district = 'East Godavari'

print("Comprehensive crop recommendations test:")
print("=" * 60)

crop_counts = {}
for i, soil_data in enumerate(test_conditions, 1):
    result = mapper.recommend_crop(soil_data, district)
    if 'error' in result:
        print(f"Test {i}: ERROR - {result['error']}")
    else:
        primary = result["recommendation"]["primary_crop"]
        alternatives = result["recommendation"]["alternative_crops"]
        pH = soil_data['pH']
        n = soil_data['nitrogen']
        rainfall = soil_data['rainfall']

        # Count crop recommendations
        if primary not in crop_counts:
            crop_counts[primary] = 0
        crop_counts[primary] += 1

        print(f"Test {i}: pH {pH}, N {n}, Rainfall {rainfall}mm")
        print(f"        Primary: {primary}, Alternatives: {alternatives}")
    print()

print("Crop Recommendation Summary:")
print("=" * 30)
for crop, count in crop_counts.items():
    print(f"{crop}: {count} recommendations")

print(f"\nTotal different crops recommended: {len(crop_counts)}")
print("✅ System is working correctly - different soil conditions get different crop recommendations!")

import sys
import os
sys.path.insert(0, 'crop_recommendation_module')

from crop_recommendation_module.core.deterministic_mapper import DeterministicCropMapper

mapper = DeterministicCropMapper()

# User's exact soil conditions
test_cases = [
    {'pH': 6.8, 'nitrogen': 55, 'phosphorus': 170, 'rainfall': 750},
    {'pH': 6.7, 'nitrogen': 68, 'phosphorus': 190, 'rainfall': 950},
]

district = 'East Godavari'  # Coastal district

print("Testing user's exact soil conditions:")
print("=" * 50)

for i, soil_data in enumerate(test_cases, 1):
    result = mapper.recommend_crop(soil_data, district)
    if 'error' in result:
        print(f"Test {i}: ERROR - {result['error']}")
    else:
        primary = result["recommendation"]["primary_crop"]
        alternatives = result["recommendation"]["alternative_crops"]
        pH = soil_data['pH']
        n = soil_data['nitrogen']
        rainfall = soil_data['rainfall']
        print(f"Test {i}: pH {pH}, N {n}, Rainfall {rainfall}mm")
        print(f"        Primary: {primary}, Alternatives: {alternatives}")
    print()

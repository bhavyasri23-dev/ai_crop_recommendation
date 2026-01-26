import sys
import os
sys.path.insert(0, 'crop_recommendation_module')

from crop_recommendation_module.core.deterministic_mapper import DeterministicCropMapper

mapper = DeterministicCropMapper()

# Test various soil conditions to see what crops are recommended
test_conditions = [
    {'pH': 6.8, 'nitrogen': 55, 'phosphorus': 170, 'rainfall': 750},
    {'pH': 6.7, 'nitrogen': 68, 'phosphorus': 190, 'rainfall': 950},
    {'pH': 7.6, 'nitrogen': 40, 'phosphorus': 150, 'rainfall': 520},
    {'pH': 6.5, 'nitrogen': 120, 'phosphorus': 80, 'rainfall': 1100},
    {'pH': 7.2, 'nitrogen': 150, 'phosphorus': 100, 'rainfall': 900},
]

district = 'East Godavari'

print("Current crop recommendations:")
print("=" * 50)

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
        print(f"Test {i}: pH {pH}, N {n}, Rainfall {rainfall}mm")
        print(f"        Primary: {primary}, Alternatives: {alternatives}")
    print()

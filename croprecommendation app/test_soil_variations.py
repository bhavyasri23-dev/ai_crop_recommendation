import sys
import os
sys.path.insert(0, 'crop_recommendation_module')

from crop_recommendation_module.core.deterministic_mapper import DeterministicCropMapper

mapper = DeterministicCropMapper()

# Test different soil conditions as provided by user
test_cases = [
    {'pH': 7.6, 'nitrogen': 40, 'phosphorus': 150, 'rainfall': 520},  # Should be Cotton
    {'pH': 6.8, 'nitrogen': 55, 'phosphorus': 170, 'rainfall': 750},  # Should be Cotton
    {'pH': 6.7, 'nitrogen': 68, 'phosphorus': 190, 'rainfall': 950},  # Should be Rice
]

district = 'East Godavari'  # Coastal district

print("Testing different soil conditions for East Godavari district:")
print("=" * 60)

for i, soil_data in enumerate(test_cases, 1):
    result = mapper.recommend_crop(soil_data, district)
    primary = result["recommendation"]["primary_crop"]
    alternatives = result["recommendation"]["alternative_crops"]
    pH = soil_data['pH']
    n = soil_data['nitrogen']
    rainfall = soil_data['rainfall']
    print(f"Test {i}: pH {pH}, N {n}, Rainfall {rainfall}mm")
    print(f"        Primary: {primary}, Alternatives: {alternatives}")
    print()

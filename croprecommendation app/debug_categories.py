import sys
import os
sys.path.insert(0, 'crop_recommendation_module')

from crop_recommendation_module.core.deterministic_mapper import DeterministicCropMapper

mapper = DeterministicCropMapper()

# Test various soil conditions to see what categories they get mapped to
test_conditions = [
    {'pH': 6.8, 'nitrogen': 55, 'phosphorus': 170, 'rainfall': 750},
    {'pH': 6.7, 'nitrogen': 68, 'phosphorus': 190, 'rainfall': 950},
    {'pH': 7.6, 'nitrogen': 40, 'phosphorus': 150, 'rainfall': 520},
    {'pH': 6.5, 'nitrogen': 120, 'phosphorus': 80, 'rainfall': 1100},
    {'pH': 7.2, 'nitrogen': 150, 'phosphorus': 100, 'rainfall': 900},
]

district = 'East Godavari'

print("Debugging soil condition categorization:")
print("=" * 60)

for i, soil_data in enumerate(test_conditions, 1):
    pH = soil_data['pH']
    nitrogen = soil_data['nitrogen']
    rainfall = soil_data['rainfall']

    # Get categories
    soil_cat = mapper._get_soil_category_from_ranges(pH)
    nutrient_cat = mapper._get_nutrient_category_from_ranges(nitrogen)
    rainfall_cat = mapper._get_rainfall_category_from_ranges(rainfall)

    fingerprint_key = f"{soil_cat}_{nutrient_cat}_{rainfall_cat}"

    # Get recommendation
    result = mapper.recommend_crop(soil_data, district)
    primary = result["recommendation"]["primary_crop"]

    print(f"Test {i}: pH {pH}, N {nitrogen}, Rainfall {rainfall}")
    print(f"        Categories: {soil_cat}, {nutrient_cat}, {rainfall_cat}")
    print(f"        Fingerprint: {fingerprint_key}")
    print(f"        Primary Crop: {primary}")
    print()

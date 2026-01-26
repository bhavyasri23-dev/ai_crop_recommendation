import sys
import os
sys.path.insert(0, 'crop_recommendation_module')

from crop_recommendation_module.core.deterministic_mapper import DeterministicCropMapper

mapper = DeterministicCropMapper()
districts = ['Anantapur', 'Srikakulam', 'Guntur', 'East Godavari', 'West Godavari', 'Chittoor', 'Krishna', 'Kurnool', 'Nellore', 'Prakasam', 'Kadapa']
soil_data = {'pH': 7.0, 'nitrogen': 80, 'phosphorus': 40, 'rainfall': 900}

print("Crop recommendations for different districts with same soil conditions:")
print("=" * 70)

for district in districts:
    result = mapper.recommend_crop(soil_data, district)
    primary = result["recommendation"]["primary_crop"]
    alternatives = result["recommendation"]["alternative_crops"]
    print(f"{district:15}: Primary: {primary}, Alternatives: {alternatives}")

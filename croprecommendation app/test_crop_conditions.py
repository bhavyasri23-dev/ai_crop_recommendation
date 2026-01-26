#!/usr/bin/env python3
"""
Test crop recommendations for specific soil conditions
"""

import sys
import os
sys.path.append('crop_recommendation_module')

from crop_recommendation_module.core.deterministic_mapper import DeterministicCropMapper

def test_crop_recommendations():
    mapper = DeterministicCropMapper()

    # Test conditions from user
    conditions1 = {'pH': 6.7, 'nitrogen': 190, 'phosphorus': 48, 'rainfall': 950}
    conditions2 = {'pH': 6.9, 'nitrogen': 180, 'phosphorus': 40, 'rainfall': 850}

    districts = ['East Godavari', 'West Godavari', 'Anantapur', 'Kurnool', 'Guntur', 'Chittoor']

    print('=== SOIL CONDITION 1: pH=6.7, N=190, P=48, Rainfall=950mm ===')
    for district in districts:
        result = mapper.recommend_crop(conditions1, district)
        print(f'{district}: {result["recommendation"]["primary_crop"]}')

    print('\n=== SOIL CONDITION 2: pH=6.9, N=180, P=40, Rainfall=850mm ===')
    for district in districts:
        result = mapper.recommend_crop(conditions2, district)
        print(f'{district}: {result["recommendation"]["primary_crop"]}')

if __name__ == "__main__":
    test_crop_recommendations()

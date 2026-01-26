#!/usr/bin/env python3
"""
Test script for specific Andhra Pradesh districts mentioned by user
"""

import sys
import os
sys.path.append('backend')

from backend.advanced_crop_prediction import advanced_predictor

# Test the specific districts mentioned by user
districts_data = {
    'Anantapur': {'features': [40, 150, 28, 220, 34, 7.6, 520], 'coords': [14.68, 77.60]},
    'Guntur': {'features': [60, 180, 40, 280, 31, 6.9, 850], 'coords': [16.30, 80.45]},
    'Prakasam': {'features': [46, 140, 30, 230, 33, 7.4, 600], 'coords': [15.83, 78.05]}
}

print('Current recommendations for problematic districts:')
print('=' * 60)

for district, data in districts_data.items():
    features = data['features']
    latitude, longitude = data['coords']
    result = advanced_predictor.predict_crop(features, latitude, longitude)
    print(f'\n{district}:')
    print(f'  Soil conditions: pH {features[5]}, N {features[0]}, P {features[1]}, K {features[2]}, temp {features[3]}, humidity {features[4]}, rainfall {features[6]}')
    print(f'  Best Crop: {result["best_crop"]}')
    print(f'  Confidence: {result["confidence"]:.1f}%')
    alternatives = [alt["crop"] for alt in result["alternatives"]]
    print(f'  Alternatives: {", ".join(alternatives)}')

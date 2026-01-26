#!/usr/bin/env python3

from backend.deterministic_mapper import DeterministicCropMapper
from backend.app import normalize_district_name

def test_district_normalization():
    mapper = DeterministicCropMapper()
    districts = mapper.get_available_districts()

    print('Available districts:')
    for d in districts:
        print(f'  {d}')

    # Test normalization
    test_cases = [
        'eastgodavari', 'East Godavari', 'EAST GODAVARI',
        'guntur', 'GUNTUR', 'Guntur',
        'vizag', 'VIZAG', 'Visakhapatnam',
        'kadapa', 'KADAPA', 'YSR Kadapa',
        'krishna', 'KRISHNA', 'Krishna',
        'kurnool', 'KURNOOL', 'Kurnool',
        'prakasam', 'PRAKASAM', 'Prakasam',
        'srikakulam', 'SRIKAKULAM', 'Srikakulam',
        'nellore', 'NELLORE', 'Nellore',
        'westgodavari', 'West Godavari', 'WEST GODAVARI',
        'chittoor', 'CHITTOOR', 'Chittoor',
        'anantapur', 'ANANTAPUR', 'Anantapur'
    ]

    print('\nNormalization tests:')
    for test in test_cases:
        normalized = normalize_district_name(test, districts)
        status = "✓" if normalized in districts else "✗"
        print(f'  {status} "{test}" -> "{normalized}"')

if __name__ == "__main__":
    test_district_normalization()

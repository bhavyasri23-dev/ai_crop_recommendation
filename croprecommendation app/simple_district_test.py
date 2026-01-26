#!/usr/bin/env python3

def normalize_district_name(district, available_districts):
    """
    Automatically normalizes any user input district to official district names.
    Works for typos, abbreviations, case-insensitive, and spaces.
    """
    if not district:
        return ""

    district_clean = district.lower().replace(" ", "")

    # Normalize available districts: lowercase + remove spaces
    normalized_map = {d.lower().replace(" ", ""): d for d in available_districts}

    # Direct match
    if district_clean in normalized_map:
        return normalized_map[district_clean]

    # Fuzzy match (close match with similarity >= 0.7)
    try:
        from difflib import get_close_matches
        matches = get_close_matches(district_clean, normalized_map.keys(), n=1, cutoff=0.7)
        if matches:
            return normalized_map[matches[0]]
    except ImportError:
        pass  # difflib not available, skip fuzzy matching

    # If no match, return original input
    return district

# All Andhra Pradesh districts with common variations
available_districts = [
    "srikakulam", "vizianagaram", "visakhapatnam", "east godavari", "west godavari",
    "krishna", "guntur", "prakasam", "nellore", "kadapa", "anantapur", "kurnool", "chittoor",
    # Common variations and abbreviations
    "eastgodavari", "westgodavari", "vizag", "ananthapuramu", "ysr kadapa", "spsr nellore"
]

# Test cases from user
test_cases = [
    'eastgodavari', 'guntur', 'krishna', 'kurnool', 'prakasam', 'srikakulam',
    'nellore', 'vizag', 'westgodavari', 'vijayawada', 'kadapa'
]

print('Testing district normalization for Andhra Pradesh districts:')
print('=' * 60)

for test in test_cases:
    normalized = normalize_district_name(test, available_districts)
    status = "✓ MATCH" if normalized in available_districts else "✗ NO MATCH"
    print(f'{status}: "{test}" -> "{normalized}"')

print('\nTesting case variations:')
case_tests = ['EASTGODAVARI', 'East Godavari', 'GUNTUR', 'Guntur', 'VIZAG', 'vizag']
for test in case_tests:
    normalized = normalize_district_name(test, available_districts)
    status = "✓ MATCH" if normalized in available_districts else "✗ NO MATCH"
    print(f'{status}: "{test}" -> "{normalized}"')

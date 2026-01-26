#!/usr/bin/env python3

import sys
import os

# Add project root to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
sys.path.insert(0, PROJECT_ROOT)

def debug_district_validation():
    """Debug the district validation logic"""

    # Import the normalization function
    from app import normalize_district_name, DISTRICT_ALIASES

    # Import mapper to get available districts
    from crop_recommendation_module.core.deterministic_mapper import DeterministicCropMapper
    mapper = DeterministicCropMapper()

    print("=== DISTRICT VALIDATION DEBUG ===")
    print()

    print("Available districts from mapper:")
    available_districts = mapper.get_available_districts()
    print(available_districts)
    print(f"Count: {len(available_districts)}")
    print()

    print("Available districts (lowercase for comparison):")
    available_lower = [d.lower() for d in available_districts]
    print(available_lower)
    print()

    print("District aliases mapping:")
    for alias, normalized in DISTRICT_ALIASES.items():
        print(f"'{alias}' -> '{normalized}'")
    print()

    # Test some common inputs
    test_inputs = [
        "anantapur",
        "Anantapur",
        "ANANTAPUR",
        "vizag",
        "Vizag",
        "VIZAG",
        "ysr",
        "YSR",
        "chittoor",
        "Chittoor",
        "CHITTOOR",
        "east godavari",
        "East Godavari",
        "EAST GODAVARI",
        "invalid_district",
        "",
        "test"
    ]

    print("Testing normalization and validation:")
    print("-" * 50)
    for test_input in test_inputs:
        normalized = normalize_district_name(test_input)
        is_valid = normalized.lower() in available_lower if normalized else False
        status = "✅ VALID" if is_valid else "❌ INVALID"
        print(f"Input: '{test_input}' -> Normalized: '{normalized}' -> {status}")

    print()
    print("=== END DEBUG ===")

if __name__ == "__main__":
    debug_district_validation()

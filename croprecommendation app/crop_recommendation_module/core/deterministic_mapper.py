import json
import os
from difflib import get_close_matches
from .soil_validator import SoilValidator

class DeterministicCropMapper:
    """
    Deterministic Crop Mapper with fuzzy district matching and aliases.
    """

    def __init__(self):
        self.validator = SoilValidator()

        # Load district data
        base = os.path.dirname(os.path.abspath(__file__))
        district_file = os.path.join(base, "../data/district_data.json")
        with open(district_file) as f:
            self.district_data = json.load(f)

        # Available districts list
        self.available_districts = list(self.district_data.keys())

        # Aliases for districts (handles typos and common nicknames)
        self.aliases = {
            # Vijayawada variants
            "vijayawada": "Krishna",
            "bezawada": "Krishna",
            "vijayaywada": "Krishna",
            "vijyawada": "Krishna",
            # Vizag variants
            "vizag": "Visakhapatnam",
            "vishakhapatnam": "Visakhapatnam",
            # Nellore variants
            "nellore": "Nellore",
            "spsr nellore": "Nellore",
            "s.p.s.r. nellore": "Nellore",
            "spsrnellore": "Nellore",
            # Other common variants
            "anantapur": "Anantapur",
            "ananthapur": "Anantapur",
            "ananthapuramu": "Anantapur",
            "kadapa": "Kadapa",
            "cuddapah": "Kadapa",
            "ysr kadapa": "Kadapa",
            "chittoor": "Chittoor",
            "chittor": "Chittoor",
            "east godavari": "East Godavari",
            "eastgodavari": "East Godavari",
            "west godavari": "West Godavari",
            "westgodavari": "West Godavari",
            "guntur": "Guntur",
            "gunthur": "Guntur",
            "prakasam": "Prakasam",
            "prakasham": "Prakasam",
            "ongole": "Prakasam",
            "kurnool": "Kurnool",
            "kurnul": "Kurnool",
            "srikakulam": "Srikakulam",
            "vizianagaram": "Vizianagaram",
            "vizianagram": "Vizianagaram",
            "vijayanagaram": "Vizianagaram"
        }

    # -----------------------------
    # Normalize district input
    # -----------------------------
    def _normalize_district(self, name: str) -> str:
        if not name:
            return "Krishna"  # default fallback

        name_lower = name.lower().strip()

        # 1️⃣ Check aliases first
        if name_lower in self.aliases:
            return self.aliases[name_lower]

        # 2️⃣ Fuzzy match against available districts
        match = get_close_matches(name.title(), self.available_districts, n=1, cutoff=0.5)
        if match:
            return match[0]

        # 3️⃣ Fallback if nothing matches
        return "Krishna"

    # -----------------------------
    # Recommend crop deterministically
    # -----------------------------
    def recommend_crop(self, soil_data: dict, district: str) -> dict:
        # Validate soil inputs
        valid, err, soil_data = self.validator.cross_validate_sources(soil_data)
        if not valid:
            return {"error": err}

        # Normalize district
        district = self._normalize_district(district)

        # Get district info from data
        district_info = self.district_data.get(district, self.district_data["Krishna"])

        # Simple deterministic crop selection based on pH and rainfall
        pH = soil_data.get("pH", 7)
        rainfall = soil_data.get("rainfall", 900)

        if rainfall >= 800 and 6 <= pH <= 7.5:
            crop = district_info["primary_crop"]
        else:
            crop = district_info["secondary_crop"]

        # Create response
        return {
            "recommendation": {
                "primary_crop": crop,
                "confidence": 0.85
            },
            "district_used": district,
            "input": soil_data
        }

    # -----------------------------
    # Get list of districts
    # -----------------------------
    def get_available_districts(self):
        return list(self.district_data.keys())

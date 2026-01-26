import json
import os
from difflib import get_close_matches
from .soil_validator import SoilValidator

class DeterministicCropMapper:
    def __init__(self):
        self.validator = SoilValidator()
        base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base, "../data/district_data.json")) as f:
            self.district_data = json.load(f)

        # All districts for fuzzy matching
        self.available_districts = list(self.district_data.keys())

        # Common aliases for districts
        self.aliases = {
            # Vijayawada aliases
            "vijayawada": "Krishna",
            "bezawada": "Krishna",
            "vijayaywada": "Krishna",
            "vijyawada": "Krishna",
            # Vizag aliases
            "vizag": "Visakhapatnam",
            "vishakhapatnam": "Visakhapatnam"
        }

    # -----------------------------
    # Normalize any district input
    # -----------------------------
    def _normalize_district(self, name: str) -> str:
        if not name:
            return "Krishna"

        name_lower = name.lower().strip()

        # 1️⃣ Check aliases first
        if name_lower in self.aliases:
            return self.aliases[name_lower]

        # 2️⃣ Fuzzy match against all districts
        close = get_close_matches(name.title(), self.available_districts, n=1, cutoff=0.6)
        if close:
            return close[0]

        # 3️⃣ Default fallback
        return "Krishna"

    # -----------------------------
    # Main deterministic recommendation
    # -----------------------------
    def recommend_crop(self, soil_data, district):
        valid, err, soil_data = self.validator.cross_validate_sources(soil_data)
        if not valid:
            return {"error": err}

        # Normalize district
        district = self._normalize_district(district)
        district_info = self.district_data.get(district, self.district_data["Krishna"])

        # Simple deterministic crop selection logic
        rainfall = soil_data.get("rainfall", 900)
        pH = soil_data.get("pH", 7)

        if rainfall >= 800 and 6 <= pH <= 7.5:
            crop = district_info["primary_crop"]
        else:
            crop = district_info["secondary_crop"]

        return {
            "recommendation": {
                "primary_crop": crop,
                "confidence": 0.85
            },
            "district_used": district,
            "input": soil_data
        }

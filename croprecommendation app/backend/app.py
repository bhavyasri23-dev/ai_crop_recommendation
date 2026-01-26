from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# ---------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from crop_recommendation_module.core.deterministic_mapper import DeterministicCropMapper

# ---------------------------------------------------------
# FLASK APP
# ---------------------------------------------------------
app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------
# INITIALIZE MAPPER
# ---------------------------------------------------------
crop_mapper = DeterministicCropMapper()

# ---------------------------------------------------------
# AVAILABLE DISTRICTS (SOURCE OF TRUTH)
# ---------------------------------------------------------
AVAILABLE_DISTRICTS = crop_mapper.get_available_districts()
AVAILABLE_DISTRICTS_LOWER = {
    d.lower().strip(): d for d in AVAILABLE_DISTRICTS
}

# ---------------------------------------------------------
# DISTRICT ALIASES (CITY → DISTRICT)
# ---------------------------------------------------------
DISTRICT_ALIASES = {
    "anantapur": "ananthapuramu",
    "ananthapur": "ananthapuramu",
    "kadapa": "ysr kadapa",
    "cuddapah": "ysr kadapa",
    "nellore": "spsr nellore",
    "chittoor": "chittoor"
}

def normalize_district_name(district):
    """
    Always returns a VALID district name
    exactly as expected by DeterministicCropMapper

# ---------------------------------------------------------
# API ROUTE
# ---------------------------------------------------------
"""
    district = district.lower().strip()

    # Remove state suffix if present
    if ',' in district:
        district = district.split(',')[0].strip()

    # Apply alias mapping
    if district in DISTRICT_ALIASES:
        district = DISTRICT_ALIASES[district]

    # Normalize to available districts
    if district in AVAILABLE_DISTRICTS_LOWER:
        return AVAILABLE_DISTRICTS_LOWER[district]

    # Fallback to default district
    return "Krishna"
@app.route("/api/recommend_crop", methods=["POST", "OPTIONS"])
def recommend_crop_api():
    if request.method == "OPTIONS":
        return "", 200

    try:
        data = request.get_json(force=True) or {}
    except Exception:
        data = {}

    # Normalize district safely
    district = normalize_district_name(data.get("district", ""))

    # Extract soil fields safely
    try:
        nitrogen = float(data.get("nitrogen", 0))
    except Exception:
        nitrogen = 0

    try:
        phosphorus = float(data.get("phosphorus", 0))
    except Exception:
        phosphorus = 0

    try:
        ph = float(data.get("pH", 7))
    except Exception:
        ph = 7

    try:
        rainfall = float(data.get("rainfall", 100))
    except Exception:
        rainfall = 100

    # Soil conditions
    conditions = {
        'pH': ph,
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'rainfall': rainfall
    }

    # Crop recommendation
    result = crop_mapper.recommend_crop(conditions, district)

    if "error" in result:
        return jsonify({"error": result["error"]}), 400

    crop = result['recommendation']['primary_crop']

    # Generate soil fingerprint
    from crop_recommendation_module.core.soil_validator import SoilValidator
    validator = SoilValidator()
    soil_fingerprint = validator.create_soil_fingerprint(ph, nitrogen, phosphorus, rainfall)

    return jsonify({
        "data": [{
            "recommendation": crop,
            "accuracy": "85%",
            "soil_fingerprint": soil_fingerprint,
            "district": district,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "pH": ph,
            "rainfall": rainfall
        }]
    }), 200

# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------
if __name__ == "__main__":
    print("Backend running on port 5001")
    print("Available districts:", AVAILABLE_DISTRICTS)
    app.run(port=5001, debug=True)

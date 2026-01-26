import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from core.deterministic_mapper import DeterministicCropMapper
from core.soil_validator import SoilValidator

# Add backend to path for IoT integration
backend_path = os.path.join(os.path.dirname(__file__), '../../backend')
sys.path.insert(0, backend_path)

try:
    from iot_integration import get_iot_sensor_data
except ImportError:
    # Fallback for when running from different directories
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
    from iot_integration import get_iot_sensor_data

# ---------------- DISTRICT NORMALIZATION ---------------- #

DISTRICT_ALIASES = {
    # Anantapur variations
    "anantapur": "Anantapur",
    "ananthapur": "Anantapur",
    "ananthapuramu": "Anantapur",

    # Kadapa variations
    "kadapa": "Kadapa",
    "cuddapah": "Kadapa",
    "ysr kadapa": "Kadapa",
    "y.s.r. kadapa": "Kadapa",
    "ysrkadapa": "Kadapa",

    # Nellore variations
    "nellore": "Nellore",
    "spsr nellore": "Nellore",
    "s.p.s.r. nellore": "Nellore",
    "spsrnellore": "Nellore",

    # Chittoor variations
    "chittoor": "Chittoor",
    "chittor": "Chittoor",

    # Vijayawada/Krishna variations
    "vijayawada": "Krishna",
    "bezawada": "Krishna",
    "vijayaywada": "Krishna",
    "vijyawada": "Krishna",
    "krishna": "Krishna",

    # Visakhapatnam variations
    "visakhapatnam": "Visakhapatnam",
    "vizag": "Visakhapatnam",
    "vishakhapatnam": "Visakhapatnam",
    "vishakapatnam": "Visakhapatnam",

    # East Godavari variations
    "east godavari": "East Godavari",
    "eastgodavari": "East Godavari",
    "e.g.": "East Godavari",
    "eg": "East Godavari",

    # West Godavari variations
    "west godavari": "West Godavari",
    "westgodavari": "West Godavari",
    "w.g.": "West Godavari",
    "wg": "West Godavari",

    # Guntur variations
    "guntur": "Guntur",
    "gunthur": "Guntur",

    # Prakasam variations
    "prakasam": "Prakasam",
    "prakasham": "Prakasam",
    "ongole": "Prakasam",

    # Kurnool variations
    "kurnool": "Kurnool",
    "kurnul": "Kurnool",

    # Srikakulam variations
    "srikakulam": "Srikakulam",

    # Vizianagaram variations
    "vizianagaram": "Vizianagaram",
    "vizianagram": "Vizianagaram",
    "vijayanagaram": "Vizianagaram"
}

def normalize_district_name(district):
    """
    Normalize district names to handle common typos and variations.
    Uses exact matches first, then fuzzy matching for close matches.
    """
    if not district:
        return ""

    district_clean = district.lower().strip()

    # First try exact matches
    if district_clean in DISTRICT_ALIASES:
        return DISTRICT_ALIASES[district_clean]

    # Try removing spaces and dots for abbreviations
    district_no_spaces = district_clean.replace(" ", "").replace(".", "")
    if district_no_spaces in DISTRICT_ALIASES:
        return DISTRICT_ALIASES[district_no_spaces]

    # Try fuzzy matching with available districts
    from difflib import get_close_matches
    available_districts = [
        "Anantapur", "Chittoor", "East Godavari", "Guntur", "Kadapa",
        "Krishna", "Kurnool", "Prakasam", "Nellore", "Srikakulam",
        "Visakhapatnam", "Vizianagaram", "West Godavari"
    ]

    # Try exact match with available districts
    if district_clean in available_districts:
        return district_clean

    # Try fuzzy matching
    matches = get_close_matches(district_clean, available_districts, n=1, cutoff=0.6)
    if matches:
        return matches[0]

    # Return original if no match found (will be validated later)
    return district_clean

# -------------------------------------------------------- #

app = Flask(__name__, static_folder='../shared_frontend')
CORS(app)

# Initialize mapper and validator (IMPORTANT: SAME NAMES USED EVERYWHERE)
mapper = DeterministicCropMapper()
soil_validator = SoilValidator()

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/recommend_crop', methods=['POST'])
def recommend_crop():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        district = data.get('district', '')
        if not district:
            return jsonify({'error': 'District is required'}), 400

        # Prioritize sensor data as primary input source
        sensor_data = None
        manual_data = None

        # Check for sensor_id to fetch IoT sensor data
        sensor_id = data.get('sensor_id')
        if sensor_id:
            try:
                sensor_response = get_iot_sensor_data(sensor_id)
                sensor_data = {
                    'pH': sensor_response['latest_reading']['ph'],
                    'nitrogen': sensor_response['latest_reading']['nitrogen'],
                    'phosphorus': sensor_response['latest_reading']['phosphorus'],
                    'rainfall': sensor_response['latest_reading']['rainfall']
                }
            except Exception as e:
                return jsonify({'error': f'Failed to fetch sensor data: {str(e)}'}), 400

        # Check for direct sensor_data input
        if not sensor_data:
            sensor_data = data.get('sensor_data')

        # Fallback to manual data if sensor data not available
        if not sensor_data:
            ph = data.get('pH', data.get('ph'))
            nitrogen = data.get('nitrogen', data.get('N'))
            phosphorus = data.get('phosphorus', data.get('P'))
            rainfall = data.get('rainfall')

            if any(v is None for v in [ph, nitrogen, phosphorus, rainfall]):
                return jsonify({
                    'error': 'Missing required soil parameters: pH, nitrogen, phosphorus, rainfall (or provide sensor_id/sensor_data)'
                }), 400

            # Validate manual soil values if provided
            validation_error = soil_validator.validate_manual_inputs(
                ph, nitrogen, phosphorus, rainfall
            )
            if validation_error:
                return jsonify({'error': validation_error}), 400

            manual_data = {
                'pH': ph,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'rainfall': rainfall
            }

        satellite_data = data.get('satellite_data')

        is_valid, error_msg, validated_data = soil_validator.cross_validate_sources(
            manual_data or {}, satellite_data, sensor_data
        )

        if not is_valid:
            return jsonify({'error': error_msg}), 400

        soil_data = {
            'pH': validated_data['pH'],
            'nitrogen': validated_data['nitrogen'],
            'phosphorus': validated_data['phosphorus'],
            'rainfall': validated_data['rainfall']
        }

        result = mapper.recommend_crop(soil_data, district)

        if 'error' in result:
            return jsonify(result), 400

        fingerprint = soil_validator.create_soil_fingerprint(
            validated_data['pH'],
            validated_data['nitrogen'],
            validated_data['phosphorus'],
            validated_data['rainfall']
        )

        return jsonify({
            'data': [{
                'recommendation': result['recommendation']['primary_crop'],
                'accuracy': f"{int(result['recommendation']['confidence'] * 100)}%",
                'soil_fingerprint': fingerprint,
                'district': district,
                'nitrogen': validated_data['nitrogen'],
                'phosphorus': validated_data['phosphorus'],
                'pH': validated_data['pH'],
                'rainfall': validated_data['rainfall']
            }]
        })

    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/api/validate_soil_data', methods=['POST'])
def validate_soil_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        manual_data = data.get('manual_data', {})
        satellite_data = data.get('satellite_data')
        sensor_data = data.get('sensor_data')

        if not manual_data:
            return jsonify({'error': 'Manual data is required'}), 400

        is_valid, error_msg, validated_data = soil_validator.cross_validate_sources(
            manual_data, satellite_data, sensor_data
        )

        response = {
            'is_valid': is_valid,
            'error_message': error_msg,
            'validated_data': validated_data if is_valid else None
        }

        if is_valid:
            response['soil_fingerprint'] = soil_validator.create_soil_fingerprint(
                validated_data['pH'],
                validated_data['nitrogen'],
                validated_data['phosphorus'],
                validated_data['rainfall']
            )

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_districts', methods=['GET'])
def get_districts():
    try:
        districts = mapper.get_available_districts()
        return jsonify({'districts': districts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_crop_characteristics', methods=['GET'])
def get_crop_characteristics():
    try:
        crop = request.args.get('crop')
        if crop:
            return jsonify({crop: mapper.get_crop_characteristics(crop)})
        return jsonify(mapper.get_all_crops())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except FileNotFoundError:
        if not path.startswith('api/'):
            return send_from_directory(app.static_folder, 'index.html')
        return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    print("Starting Crop Recommendation API on localhost:5002")
    print("Available districts:", mapper.get_available_districts())
    app.run(debug=True, host='0.0.0.0', port=5002, use_reloader=False)

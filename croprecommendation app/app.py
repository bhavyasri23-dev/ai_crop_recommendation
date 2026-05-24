from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import io

# Import from your packages
from crop_recommendation_module.core.deterministic_mapper import DeterministicCropMapper
from crop_recommendation_module.core.soil_validator import SoilValidator
from crop_recommendation import CropRecommender
from disease_detection_module.core.single_output_detector import disease_detector
from disease_detection_module.core.image_processor import image_processor
from disease_detection_module.core.disease_suggestions import disease_suggestions


def create_app():
    app = Flask(__name__, static_folder='shared_frontend')
    CORS(app)

    mapper = DeterministicCropMapper()
    soil_validator = SoilValidator()
    recommender = CropRecommender()

    def calibrate_accuracy(score):
        """
        Map suitability score (0-100) to a conservative accuracy percentage (40-95).
        """
        try:
            score = float(score)
        except (TypeError, ValueError):
            return 0

        score = max(0.0, min(100.0, score))
        accuracy = 40.0 + (score * 0.55)
        accuracy = max(40.0, min(95.0, accuracy))
        return int(round(accuracy))

    @app.route("/status", methods=["GET"])
    def home():
        return jsonify({
            "status": "ok",
            "message": "AI Crop Recommendation & Disease Detection System is running on port 5002"
        })

    @app.route("/api/recommend_crop", methods=["POST"])
    def recommend_crop():
        data = request.get_json(force=True, silent=True) or {}

        district_raw = data.get("district", "")
        district = mapper._normalize_district(district_raw)

        def safe(val, default):
            try:
                return float(val)
            except (TypeError, ValueError):
                return default

        # Accept both short and full field names
        soil_ph = safe(data.get("pH", data.get("ph")), 7.0)
        nitrogen = safe(data.get("nitrogen", data.get("N")), 50.0)
        phosphorus = safe(data.get("phosphorus", data.get("P")), 30.0)
        potassium = safe(data.get("potassium", data.get("K")), 40.0)
        moisture = safe(data.get("moisture", data.get("humidity")), 50.0)
        temperature = safe(data.get("temperature", data.get("temp")), 28.0)
        rainfall = safe(data.get("rainfall"), 900.0)

        validation_error = soil_validator.validate_manual_inputs(
            soil_ph, nitrogen, phosphorus, rainfall
        )
        if validation_error:
            return jsonify({"error": validation_error}), 400

        # Use the richer scoring recommender and return TOP-1 deterministically
        recommender.rainfall_mm = rainfall
        result = recommender.recommend_crops(
            soil_ph,
            moisture,
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            district,
            top_n=1
        )

        if not result.get("recommendations"):
            return jsonify({"error": "No suitable crop found"}), 400

        top = result["recommendations"][0]
        soil_fingerprint = soil_validator.create_soil_fingerprint(
            soil_ph, nitrogen, phosphorus, rainfall
        )

        return jsonify({
            "data": [{
                "recommendation": top["crop"],
                "accuracy": f"{calibrate_accuracy(top['suitability_score'])}%",
                "reason": top.get("reason", ""),
                "soil_fingerprint": soil_fingerprint,
                "district": district,
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "pH": soil_ph,
                "moisture": moisture,
                "temperature": temperature,
                "rainfall": rainfall
            }]
        }), 200

    @app.route('/api/detect_disease', methods=['POST'])
    def detect_disease():
        """
        Disease detection endpoint
        Returns exactly one result: disease name or "Healthy"
        """
        try:
            # Check if image is provided as file upload or base64
            image_data = None
            json_data = None
            
            if 'image' in request.files:
                # Handle file upload - read ONCE and store
                image_file = request.files['image']
                if image_file.filename == '':
                    return jsonify({'error': 'No image file selected'}), 400

                # Read the file data
                image_data = image_file.read()

            elif request.is_json:
                # Handle base64 encoded image
                json_data = request.get_json()
                if not json_data or 'image' not in json_data:
                    return jsonify({'error': 'No image data provided'}), 400

                try:
                    # Remove data URL prefix if present
                    image_b64 = json_data['image']
                    if ',' in image_b64:
                        image_b64 = image_b64.split(',')[1]

                    image_data = base64.b64decode(image_b64)
                except Exception as e:
                    return jsonify({'error': f'Invalid base64 image data: {str(e)}'}), 400
            else:
                return jsonify({'error': 'No image provided. Use file upload or base64 JSON'}), 400

            # Validate we have image data
            if not image_data or len(image_data) == 0:
                return jsonify({'error': 'Empty image data received'}), 400

            # Get optional crop type - use cached json_data
            crop_type = None
            if json_data is not None:
                crop_type = json_data.get('crop_type')
            elif 'crop_type' in request.form:
                crop_type = request.form['crop_type']

            # Validate crop type if provided
            if crop_type and not disease_detector.validate_crop_type(crop_type):
                return jsonify({
                    'error': f'Unsupported crop type: {crop_type}',
                    'supported_crops': disease_detector.get_supported_crops()
                }), 400

            # Perform single-output disease detection
            result = disease_detector.predict_single_output(image_data, crop_type)

            # Format response
            if result['prediction'] == 'Error':
                return jsonify({
                    'error': result.get('error', 'Unknown error'),
                    'status': 'failed'
                }), 400

            response = {
                'data': {
                    'prediction': result['prediction'],
                    'confidence': result['confidence'],
                    'crop_type': result['crop_type'],
                    'model_used': result.get('model_used', 'Unknown'),
                    'processing_status': result.get('processing_status', 'unknown')
                }
            }

            # Add additional info for uncertain predictions
            if result['prediction'] == 'Uncertain':
                response['data']['top_prediction'] = result.get('top_prediction')
                response['data']['note'] = 'Prediction confidence too low for reliable diagnosis'

            # Add treatment suggestions
            if result['prediction'] == 'Healthy':
                suggestions = disease_suggestions.get_healthy_suggestions()
            else:
                # Get treatment preference from request (default to balanced)
                treatment_preference = None
                if json_data is not None:
                    treatment_preference = json_data.get('treatment_preference', 'balanced')
                elif 'treatment_preference' in request.form:
                    treatment_preference = request.form['treatment_preference']
                else:
                    treatment_preference = 'balanced'

                if not treatment_preference:
                    treatment_preference = 'balanced'

                suggestions = disease_suggestions.get_suggestions(result['prediction'], treatment_preference)

            response['data']['suggestions'] = suggestions

            return jsonify(response)

        except Exception as e:
            return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

    @app.route('/api/get_supported_crops', methods=['GET'])
    def get_supported_crops():
        """
        Get list of supported crop types for disease detection
        """
        try:
            crops = disease_detector.get_supported_crops()
            crop_diseases = {}

            for crop in crops:
                crop_diseases[crop] = disease_detector.get_crop_diseases(crop)

            return jsonify({
                'supported_crops': crops,
                'crop_diseases': crop_diseases
            })

        except Exception as e:
            return jsonify({'error': f'Error retrieving supported crops: {str(e)}'}), 500

    # Serve static files from shared_frontend directory
    @app.route('/', defaults={'path': 'index.html'})
    @app.route('/<path:path>')
    def serve_static(path):
        # Don't serve static files for API routes
        if path.startswith('api/'):
            return jsonify({'error': 'API endpoint not found'}), 404

        try:
            return send_from_directory(app.static_folder, path)
        except FileNotFoundError:
            # If file not found, serve index.html for client-side routing
            try:
                return send_from_directory(app.static_folder, 'index.html')
            except FileNotFoundError:
                return jsonify({'error': 'File not found'}), 404

    return app


if __name__ == "__main__":
    app = create_app()
    print("AI Crop Recommendation & Disease Detection System")
    print("Server running on http://127.0.0.1:5002")
    print("Supported crops for disease detection:", disease_detector.get_supported_crops())
    app.run(host="127.0.0.1", port=5002, debug=False)

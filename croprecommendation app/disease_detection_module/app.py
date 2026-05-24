"""
Independent Disease Detection Module
Provides single-output disease detection: exactly one disease name or "Healthy" per image
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import atexit

# Core modules
from core.single_output_detector import disease_detector
from core.image_processor import image_processor
from core.disease_suggestions import disease_suggestions
from core.model_manager import model_manager

app = Flask(__name__, static_folder='../shared_frontend')
CORS(app)  # Enable CORS for all routes

# ---- Temporary request logging (to debug 405/404 issues) ----
@app.before_request
def log_incoming_request():
    try:
        print(f"[disease-module] Incoming request: {request.method} {request.path} (Content-Type: {request.content_type})")
    except Exception:
        pass

# -------------------
# TensorFlow cleanup
# -------------------
def cleanup_tensorflow():
    """Cleanup TensorFlow resources on shutdown"""
    try:
        model_manager.close()
        import tensorflow as tf
        tf.keras.backend.clear_session()
    except Exception:
        pass

atexit.register(cleanup_tensorflow)

# -------------------
# Error handlers
# -------------------
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# -------------------
# Disease detection endpoint
# -------------------
@app.route('/api/detect_disease', methods=['POST'])
def detect_disease():
    """
    Single-output disease detection
    Returns exactly one result: disease name or "Healthy"
    """
    try:
        image_data = None
        json_data = None

        # -------------------
        # Get image
        # -------------------
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename == '':
                return jsonify({'error': 'No image file selected'}), 400
            image_data = image_file.read()

        elif request.is_json:
            json_data = request.get_json()
            if not json_data or 'image' not in json_data:
                return jsonify({'error': 'No image data provided'}), 400
            try:
                image_b64 = json_data['image']
                if ',' in image_b64:
                    image_b64 = image_b64.split(',')[1]
                image_data = base64.b64decode(image_b64)
            except Exception as e:
                return jsonify({'error': f'Invalid base64 image data: {str(e)}'}), 400
        else:
            return jsonify({'error': 'No image provided. Use file upload or base64 JSON'}), 400

        if not image_data or len(image_data) == 0:
            return jsonify({'error': 'Empty image data received'}), 400

        # -------------------
        # Crop type (optional)
        # -------------------
        crop_type = None
        if json_data is not None:
            crop_type = json_data.get('crop_type')
        elif 'crop_type' in request.form:
            crop_type = request.form['crop_type']

        # -------------------
        # Warn if unknown crop
        # -------------------
        if crop_type and not disease_detector.validate_crop_type(crop_type):
            print(f"WARNING: Crop type '{crop_type}' unknown, using general detection")

        # -------------------
        # Prediction
        # -------------------
        result = disease_detector.predict_single_output(image_data, crop_type)

        if result.get('prediction') == 'Error':
            return jsonify({'error': result.get('error', 'Unknown error'), 'status': 'failed'}), 400

        # -------------------
        # Prepare response
        # -------------------
        response = {
            'data': {
                'prediction': result['prediction'],
                'confidence': result.get('confidence', 0.0),
                'crop_type': result.get('crop_type', 'unknown'),
                'model_used': result.get('model_used', 'disease_model'),
                'processing_status': result.get('processing_status', 'success')
            }
        }

        # Add info for uncertain predictions
        if result['prediction'] == 'Uncertain':
            response['data']['top_prediction'] = result.get('top_prediction')
            response['data']['note'] = result.get('reason', 'Prediction confidence too low')

        # Add treatment suggestions
        if result['prediction'] == 'Healthy':
            suggestions = disease_suggestions.get_healthy_suggestions()
        else:
            # Check for treatment preference
            treatment_preference = None
            if json_data:
                treatment_preference = json_data.get('treatment_preference', 'balanced')
            elif 'treatment_preference' in request.form:
                treatment_preference = request.form['treatment_preference']
            else:
                treatment_preference = 'balanced'

            suggestions = disease_suggestions.get_suggestions(result['prediction'], treatment_preference)

        response['data']['suggestions'] = suggestions

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

# -------------------
# Supported crops endpoint
# -------------------
@app.route('/api/get_supported_crops', methods=['GET'])
def get_supported_crops():
    try:
        crops = disease_detector.get_supported_crops()
        crop_diseases = {crop: disease_detector.get_crop_diseases(crop) for crop in crops}
        return jsonify({'supported_crops': crops, 'crop_diseases': crop_diseases})
    except Exception as e:
        return jsonify({'error': f'Error retrieving supported crops: {str(e)}'}), 500

# -------------------
# Image validation endpoint
# -------------------
@app.route('/api/validate_image', methods=['POST'])
def validate_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400

        image_data = image_file.read()

        validation_error = image_processor.validate_image(image_data)
        if validation_error:
            return jsonify({'is_valid': False, 'error': validation_error})

        features = image_processor.extract_image_features(image_data)
        is_leaf, leaf_conf = image_processor.is_leaf_image(image_data)

        return jsonify({
            'is_valid': True,
            'appears_to_be_leaf': is_leaf,
            'leaf_confidence': leaf_conf,
            'image_features': features
        })
    except Exception as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 500

# -------------------
# Serve frontend
# -------------------
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except FileNotFoundError:
        if not path.startswith('api/'):
            return send_from_directory(app.static_folder, 'index.html')
        return jsonify({'error': 'File not found'}), 404

# -------------------
# Start server
# -------------------
if __name__ == '__main__':
    print("Starting Independent Disease Detection Module...")
    print("Supported crops:", disease_detector.get_supported_crops())
    print("Disease model loaded:", getattr(disease_detector, 'model', None) is not None)
    app.run(debug=True, host='0.0.0.0', port=5003, use_reloader=False)

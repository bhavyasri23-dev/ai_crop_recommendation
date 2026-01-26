"""
Standalone Disease Detection Module using Pattern-Based Detection
No TensorFlow/Keras dependencies - uses OpenCV and custom algorithms
Runs on port 5001
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import cv2
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)

# Plant and disease classes
PLANT_CLASSES = ['corn', 'rice', 'wheat', 'tomato', 'cucumber', 'potato', 'soybean', 'apple']

DISEASE_CLASSES = {
    'corn': ['healthy', 'Common_rust', 'Northern_Leaf_Blight', 'Cercospora_leaf_spot'],
    'rice': ['healthy', 'Brown_spot', 'Leaf_smut', 'Bacterial_blight'],
    'wheat': ['healthy', 'Powdery_mildew', 'Leaf_rust', 'Septoria'],
    'tomato': ['healthy', 'Early_blight', 'Late_blight', 'Leaf_Mold', 'Septoria_leaf_spot'],
    'cucumber': ['healthy', 'Powdery_mildew', 'Downy_mildew', 'Bacterial_wilt', 'Angular_leaf_spot'],
    'potato': ['healthy', 'Early_blight', 'Late_blight'],
    'soybean': ['healthy', 'Bacterial_blight', 'Brown_spot'],
    'apple': ['healthy', 'Apple_scab', 'Black_rot', 'Cedar_apple_rust']
}

# Treatment database
TREATMENT_DATABASE = {
    'corn': {
        'healthy': 'Plant is healthy. Continue regular maintenance.',
        'Common_rust': 'Apply fungicide containing azoxystrobin or propiconazole. Remove infected leaves.',
        'Northern_Leaf_Blight': 'Use resistant varieties. Apply chlorothalonil fungicide.',
        'Cercospora_leaf_spot': 'Apply copper-based fungicides. Improve air circulation.'
    },
    'rice': {
        'healthy': 'Plant is healthy. Continue regular maintenance.',
        'Brown_spot': 'Apply silicon fertilizers. Use resistant varieties.',
        'Leaf_smut': 'Treat seeds with fungicide before planting.',
        'Bacterial_blight': 'Use copper-based bactericides. Avoid overhead irrigation.'
    },
    'wheat': {
        'healthy': 'Plant is healthy. Continue regular maintenance.',
        'Powdery_mildew': 'Apply sulfur-based fungicides. Improve air circulation.',
        'Leaf_rust': 'Use resistant varieties. Apply triazole fungicides.',
        'Septoria': 'Apply azole fungicides. Remove crop residues.'
    },
    'tomato': {
        'healthy': 'Plant is healthy. Continue regular maintenance.',
        'Early_blight': 'Apply copper fungicides. Mulch around plants.',
        'Late_blight': 'Remove infected plants immediately. Apply systemic fungicides.',
        'Leaf_Mold': 'Improve air circulation. Apply chlorothalonil fungicide.',
        'Septoria_leaf_spot': 'Apply copper fungicides. Avoid overhead watering.'
    },
    'cucumber': {
        'healthy': 'Plant is healthy. Continue regular maintenance.',
        'Powdery_mildew': 'Apply sulfur or potassium bicarbonate sprays.',
        'Downy_mildew': 'Apply copper fungicides. Avoid overhead watering.',
        'Bacterial_wilt': 'Remove infected plants. Control cucumber beetles.',
        'Angular_leaf_spot': 'Apply copper fungicides. Use disease-free seeds.'
    },
    'potato': {
        'healthy': 'Plant is healthy. Continue regular maintenance.',
        'Early_blight': 'Apply copper fungicides. Mulch around plants.',
        'Late_blight': 'Remove infected plants. Apply systemic fungicides.'
    },
    'soybean': {
        'healthy': 'Plant is healthy. Continue regular maintenance.',
        'Bacterial_blight': 'Use copper bactericides. Plant resistant varieties.',
        'Brown_spot': 'Apply foliar fungicides. Improve drainage.'
    },
    'apple': {
        'healthy': 'Plant is healthy. Continue regular maintenance.',
        'Apple_scab': 'Remove infected leaves and apply fungicide. Prune affected branches.',
        'Black_rot': 'Prune infected branches and apply fungicide. Remove fallen leaves.',
        'Cedar_apple_rust': 'Remove nearby cedar trees and apply fungicide.'
    }
}

def decode_image(image_data):
    """Decode image from base64 or file data"""
    if isinstance(image_data, str):
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
    else:
        image_bytes = image_data
    
    # Convert to OpenCV format
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

def identify_plant_type(image):
    """Identify plant type based on color and texture analysis"""
    if image is None:
        return 'unknown', 0.5
    
    # Convert to HSV for color analysis
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate average color values
    avg_hue = np.mean(hsv[:, :, 0])
    avg_saturation = np.mean(hsv[:, :, 1])
    avg_value = np.mean(hsv[:, :, 2])
    
    # Simple rule-based classification
    if avg_value > 180:  # Very bright - might be wheat or rice
        return 'wheat', 0.7
    elif avg_hue < 15 and avg_saturation > 150:  # Deep red - apple
        return 'apple', 0.8
    elif avg_hue < 30 and avg_saturation > 100:  # Reddish - tomato
        return 'tomato', 0.75
    elif avg_hue > 60 and avg_hue < 90:  # Greenish - corn or cucumber
        height, width = image.shape[:2]
        aspect_ratio = width / height
        if aspect_ratio > 1.5:
            return 'corn', 0.7
        else:
            return 'cucumber', 0.7
    else:
        # Check for potato/soybean (darker greens)
        if avg_value < 100:
            return 'potato', 0.6
        return 'soybean', 0.6

def detect_disease(image, plant_type):
    """Detect disease based on color analysis for spots and discoloration"""
    if plant_type == 'unknown' or image is None:
        return 'unknown', 0.5
    
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Look for disease indicators
    # Brown/yellow spots indicate disease
    brown_mask = cv2.inRange(hsv, (5, 50, 50), (15, 255, 255))
    yellow_mask = cv2.inRange(hsv, (20, 100, 100), (30, 255, 255))
    
    disease_pixels = np.sum(brown_mask > 0) + np.sum(yellow_mask > 0)
    total_pixels = image.shape[0] * image.shape[1]
    disease_ratio = disease_pixels / total_pixels
    
    if disease_ratio > 0.1:
        diseases = DISEASE_CLASSES.get(plant_type, ['healthy'])
        if len(diseases) > 1:
            return diseases[1], 0.8
        return 'healthy', 0.9
    else:
        return 'healthy', 0.85

def get_healthy_suggestions():
    """Get suggestions for healthy plants"""
    return {
        'maintenance_tips': [
            'Continue regular watering schedule',
            'Monitor for any early signs of disease',
            'Maintain proper fertilization schedule',
            'Ensure adequate sunlight exposure'
        ],
        'prevention_tips': [
            'Rotate crops seasonally',
            'Remove any dead plant material promptly',
            'Maintain good air circulation between plants',
            'Use mulch to retain soil moisture'
        ],
        'monitoring_advice': [
            'Check leaves weekly for any discoloration',
            'Inspect undersides of leaves for pests',
            'Record growth progress for future reference'
        ]
    }

def get_disease_suggestions(disease_name, treatment_preference='balanced'):
    """Get treatment suggestions for diseased plants"""
    # Parse plant type and disease from prediction
    plant_type = None
    for plant, diseases in DISEASE_CLASSES.items():
        if disease_name in diseases:
            plant_type = plant
            break
    
    if not plant_type:
        return {
            'error': 'Unknown disease',
            'general_advice': [
                'Consult local agricultural extension service',
                'Take sample to local plant clinic',
                'Search online databases for matching symptoms'
            ]
        }
    
    treatment = TREATMENT_DATABASE.get(plant_type, {}).get(disease_name, 'Consult local agricultural expert.')
    
    suggestions = {
        'immediate_actions': [treatment],
        'preventive_measures': [
            f'Use disease-free seeds for {plant_type}',
            'Practice crop rotation',
            'Remove and destroy infected plant parts',
            'Sanitize tools after working with infected plants'
        ]
    }
    
    if treatment_preference in ['organic', 'balanced']:
        suggestions['organic_options'] = [
            'Apply neem oil spray',
            'Use copper-based organic fungicides',
            'Apply baking soda solution (1 tbsp/gal)',
            'Introduce beneficial insects'
        ]
    
    if treatment_preference in ['chemical', 'balanced']:
        suggestions['chemical_options'] = [
            'Apply systemic fungicide as directed',
            'Use contact fungicides for prevention',
            'Consider resistant varieties for future planting'
        ]
    
    return suggestions

@app.route('/api/detect_disease', methods=['POST'])
def detect_disease_endpoint():
    """Main disease detection endpoint"""
    try:
        # Get image data
        image_data = None
        json_data = None
        
        if 'image' in request.files:
            image_file = request.files['image']
            image_data = image_file.read()
        elif request.is_json:
            json_data = request.get_json()
            if json_data and 'image' in json_data:
                try:
                    image_b64 = json_data['image']
                    if ',' in image_b64:
                        image_b64 = image_b64.split(',')[1]
                    image_data = base64.b64decode(image_b64)
                except Exception as e:
                    return jsonify({'error': f'Invalid base64: {str(e)}'}), 400
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        if not image_data or len(image_data) == 0:
            return jsonify({'error': 'Empty image data'}), 400
        
        # Get optional crop type
        crop_type = None
        if json_data:
            crop_type = json_data.get('crop_type')
        if 'crop_type' in request.form:
            crop_type = request.form['crop_type']
        
        treatment_preference = 'balanced'
        if json_data and 'treatment_preference' in json_data:
            treatment_preference = json_data['treatment_preference']
        
        # Decode and process image
        image = decode_image(image_data)
        if image is None:
            return jsonify({'error': 'Could not decode image'}), 400
        
        # Identify plant type (or use provided crop_type)
        if crop_type and crop_type.lower() in PLANT_CLASSES:
            plant_type = crop_type.lower()
            plant_confidence = 0.95
        else:
            plant_type, plant_confidence = identify_plant_type(image)
        
        if plant_type == 'unknown':
            return jsonify({
                'error': 'Could not identify plant type',
                'suggestion': 'Try specifying crop_type in your request'
            }), 400
        
        # Detect disease
        disease_name, disease_confidence = detect_disease(image, plant_type)
        
        final_confidence = min(plant_confidence, disease_confidence)
        
        # Get suggestions
        if disease_name == 'healthy':
            suggestions = get_healthy_suggestions()
        else:
            suggestions = get_disease_suggestions(disease_name, treatment_preference)
        
        return jsonify({
            'data': {
                'prediction': disease_name.replace('_', ' ').title(),
                'confidence': final_confidence,
                'crop_type': plant_type.capitalize(),
                'model_used': 'Pattern-based detection',
                'suggestions': suggestions
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/get_supported_crops', methods=['GET'])
def get_supported_crops():
    """Get supported crops and diseases"""
    crops = list(DISEASE_CLASSES.keys())
    crop_diseases = {crop: [d.replace('_', ' ').title() for d in diseases] for crop, diseases in DISEASE_CLASSES.items()}
    return jsonify({
        'supported_crops': crops,
        'crop_diseases': crop_diseases
    })

if __name__ == '__main__':
    print("Starting Disease Detection Module on port 5001...")
    print("Supported crops:", PLANT_CLASSES)
    print("Using pattern-based detection (no TensorFlow)")
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)


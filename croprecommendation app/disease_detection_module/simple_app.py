"""
Simple Disease Detection Module using PIL and color analysis
No TensorFlow/OpenCV dependencies
Runs on port 5001
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from PIL import Image
import io
import statistics

app = Flask(__name__)
CORS(app)

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

def rgb_to_hsv(r, g, b):
    r, g, b = r/255, g/255, b/255
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c
    
    if diff == 0:
        h = 0
    elif max_c == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif max_c == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360
    
    s = 0 if max_c == 0 else (diff / max_c) * 100
    v = max_c * 100
    
    return h, s, v

def decode_image(image_data):
    if isinstance(image_data, str):
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
    else:
        image_bytes = image_data
    image = Image.open(io.BytesIO(image_bytes))
    return image.convert('RGB')

def analyze_image_colors(image):
    pixels = list(image.getdata())
    hsv_values = [rgb_to_hsv(p[0], p[1], p[2]) for p in pixels]
    
    h_values = [h for h, s, v in hsv_values]
    s_values = [s for h, s, v in hsv_values]
    v_values = [v for h, s, v in hsv_values]
    
    return {
        'avg_hue': statistics.mean(h_values),
        'avg_saturation': statistics.mean(s_values),
        'avg_value': statistics.mean(v_values),
        'median_hue': statistics.median(h_values),
        'median_saturation': statistics.median(s_values),
        'median_value': statistics.median(v_values)
    }

def identify_plant_type(image):
    colors = analyze_image_colors(image)
    hue = colors['avg_hue']
    sat = colors['avg_saturation']
    val = colors['avg_value']
    
    if val > 65:  # Very bright
        return 'wheat', 0.7
    elif hue < 15 and sat > 50:  # Reddish - apple
        return 'apple', 0.8
    elif hue < 30 and sat > 40:  # Red/orange - tomato
        return 'tomato', 0.75
    elif 30 < hue < 90:  # Greenish
        width, height = image.size
        aspect_ratio = width / height
        if aspect_ratio > 1.5:
            return 'corn', 0.7
        else:
            return 'cucumber', 0.7
    else:
        if val < 40:
            return 'potato', 0.6
        return 'soybean', 0.6

def detect_disease(image, plant_type):
    colors = analyze_image_colors(image)
    
    # Look for disease indicators (brown/yellow spots)
    # Low saturation with medium value often indicates browning
    if colors['avg_saturation'] < 25 and colors['avg_value'] < 70:
        diseases = DISEASE_CLASSES.get(plant_type, ['healthy'])
        return diseases[1] if len(diseases) > 1 else 'healthy', 0.7
    
    return 'healthy', 0.85

@app.route('/api/detect_disease', methods=['POST'])
def detect_disease_endpoint():
    try:
        image_data = None
        json_data = None
        
        if 'image' in request.files:
            image_data = request.files['image'].read()
        elif request.is_json:
            json_data = request.get_json()
            if json_data and 'image' in json_data:
                try:
                    b64 = json_data['image']
                    if ',' in b64:
                        b64 = b64.split(',')[1]
                    image_data = base64.b64decode(b64)
                except Exception as e:
                    return jsonify({'error': f'Invalid base64: {str(e)}'}), 400
        
        if not image_data or len(image_data) == 0:
            return jsonify({'error': 'No image provided'}), 400
        
        crop_type = None
        if json_data:
            crop_type = json_data.get('crop_type')
        
        image = decode_image(image_data)
        if image is None:
            return jsonify({'error': 'Could not decode image'}), 400
        
        if crop_type and crop_type.lower() in PLANT_CLASSES:
            plant_type = crop_type.lower()
            plant_conf = 0.95
        else:
            plant_type, plant_conf = identify_plant_type(image)
        
        if plant_type == 'unknown':
            return jsonify({'error': 'Could not identify plant. Try specifying crop_type.'}), 400
        
        disease_name, disease_conf = detect_disease(image, plant_type)
        confidence = min(plant_conf, disease_conf)
        
        return jsonify({
            'data': {
                'prediction': disease_name.replace('_', ' ').title(),
                'confidence': confidence,
                'crop_type': plant_type.capitalize(),
                'model_used': 'Color-based pattern detection',
                'suggestions': {
                    'immediate_actions': ['Consult local agricultural expert'],
                    'preventive_measures': ['Practice crop rotation', 'Use disease-free seeds']
                }
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_supported_crops', methods=['GET'])
def get_supported_crops():
    crops = list(DISEASE_CLASSES.keys())
    crop_diseases = {c: [d.replace('_', ' ').title() for d in DISEASE_CLASSES[c]] for c in crops}
    return jsonify({'supported_crops': crops, 'crop_diseases': crop_diseases})

if __name__ == '__main__':
    print("Starting Disease Detection on port 5001...")
    print("Color-based pattern detection (no TensorFlow/OpenCV)")
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import joblib
import numpy as np
import cv2
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='../web_app')
CORS(app)  # Enable CORS for all routes

# Load models with error handling (intentionally skip TensorFlow for testing)
crop_model = None
yield_model = None
profit_model = None
disease_model = None
disease_classes = []

# Comprehensive disease classes for fallback
comprehensive_disease_classes = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___healthy', 'Cherry_(including_sour)___Powdery_mildew',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___healthy', 'Corn_(maize)___Northern_Leaf_Blight',
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___healthy', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
    'Potato___Early_blight', 'Potato___healthy', 'Potato___Late_blight',
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___healthy', 'Strawberry___Leaf_scorch',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___healthy', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_mosaic_virus', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus'
]

# Force models to not load for testing fallback functionality
models_loaded = False
print("Testing mode: Skipping ML model loading to test fallback functionality")

# Load disease classes for fallback
disease_classes = comprehensive_disease_classes
print(f"Loaded {len(disease_classes)} disease classes for fallback testing")

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.route('/api/predict_crop', methods=['POST'])
def predict_crop():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # Validate and extract features
        required_keys = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        features = []

        for key in required_keys:
            if key not in data:
                return jsonify({'error': f'Missing required field: {key}'}), 400
            try:
                value = float(data[key])
                # Validate ranges for agricultural parameters
                if key == 'N' and not (0 <= value <= 200):
                    return jsonify({'error': f'Nitrogen (N) should be between 0-200 kg/ha'}), 400
                elif key == 'P' and not (0 <= value <= 150):
                    return jsonify({'error': f'Phosphorus (P) should be between 0-150 kg/ha'}), 400
                elif key == 'K' and not (0 <= value <= 300):
                    return jsonify({'error': f'Potassium (K) should be between 0-300 kg/ha'}), 400
                elif key == 'temperature' and not (10 <= value <= 50):
                    return jsonify({'error': f'Temperature should be between 10-50°C'}), 400
                elif key == 'humidity' and not (0 <= value <= 100):
                    return jsonify({'error': f'Humidity should be between 0-100%'}), 400
                elif key == 'ph' and not (3.5 <= value <= 9.0):
                    return jsonify({'error': f'pH should be between 3.5-9.0'}), 400
                elif key == 'rainfall' and not (0 <= value <= 1000):
                    return jsonify({'error': f'Rainfall should be between 0-1000 mm'}), 400
                features.append(value)
            except ValueError:
                return jsonify({'error': f'Invalid type for {key}: must be numeric'}), 400

        # Convert to DataFrame with proper column names for sklearn
        import pandas as pd
        features_df = pd.DataFrame([features], columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])

        prediction = 'Unknown'
        confidence = 0.0
        alternatives = []

        if models_loaded and crop_model is not None:
            try:
                # Get prediction probabilities if available
                if hasattr(crop_model, 'predict_proba'):
                    probabilities = crop_model.predict_proba(features_df)[0]
                    confidence = round(float(max(probabilities)) * 100, 2)

                    # Get top 3 predictions
                    top_indices = np.argsort(probabilities)[-3:][::-1]
                    crop_classes = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean', 'Barley']
                    prediction = crop_classes[top_indices[0]]

                    # Add alternatives
                    for i in range(1, min(3, len(top_indices))):
                        alt_crop = crop_classes[top_indices[i]]
                        alt_conf = round(float(probabilities[top_indices[i]]) * 100, 2)
                        alternatives.append({'crop': alt_crop, 'confidence': alt_conf})
                else:
                    prediction = crop_model.predict(features_df)[0]
                    confidence = 85.0  # Default confidence for models without predict_proba

            except Exception as e:
                print(f"Model prediction failed: {e}, using intelligent fallback")
                prediction, confidence, alternatives = intelligent_crop_prediction(features)
        else:
            # Use intelligent prediction when model is not available
            prediction, confidence, alternatives = intelligent_crop_prediction(features)

        # Get location-specific recommendations if latitude/longitude provided
        location_recommendations = {}
        if 'latitude' in data and 'longitude' in data:
            try:
                lat = float(data['latitude'])
                lon = float(data['longitude'])
                location_recommendations = get_location_based_recommendations(lat, lon, features)
            except:
                pass

        return jsonify({
            'predicted_crop': prediction,
            'confidence': confidence,
            'alternatives': alternatives,
            'location_recommendations': location_recommendations,
            'input_summary': {
                'nitrogen': features[0],
                'phosphorus': features[1],
                'potassium': features[2],
                'temperature': features[3],
                'humidity': features[4],
                'ph': features[5],
                'rainfall': features[6]
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict_disease', methods=['POST'])
def predict_disease():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Read image data once and store it
        image_data = file.read()
        img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({'error': 'Invalid image file'}), 400

        # Use enhanced pattern detection for testing
        predicted_disease, confidence = enhanced_disease_detection(img)
        model_used = 'enhanced_pattern'

        # Define comprehensive cure information based on disease
        cure_info = {
            'Apple___Apple_scab': 'Remove infected leaves and apply fungicide like captan. Prune affected branches.',
            'Apple___Black_rot': 'Prune infected branches and apply fungicide. Remove fallen leaves.',
            'Apple___Cedar_apple_rust': 'Remove nearby cedar trees and apply fungicide. Improve air circulation.',
            'Apple___healthy': 'No cure needed, plant is healthy.',
            'Blueberry___healthy': 'No cure needed, plant is healthy.',
            'Cherry_(including_sour)___healthy': 'No cure needed, plant is healthy.',
            'Cherry_(including_sour)___Powdery_mildew': 'Apply sulfur-based fungicide. Improve air circulation.',
            'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Apply fungicide and rotate crops. Remove infected leaves.',
            'Corn_(maize)___Common_rust_': 'Apply fungicide and plant resistant varieties.',
            'Corn_(maize)___healthy': 'No cure needed, plant is healthy.',
            'Corn_(maize)___Northern_Leaf_Blight': 'Apply fungicide and remove infected leaves.',
            'Cucumber___Powdery_mildew': 'Apply sulfur-based fungicide. Improve air circulation and spacing between plants.',
            'Cucumber___Downy_mildew': 'Apply fungicide and improve air circulation. Avoid overhead watering.',
            'Cucumber___Bacterial_wilt': 'Remove infected plants immediately. Control cucumber beetles.',
            'Cucumber___Angular_leaf_spot': 'Apply copper-based fungicide. Avoid working with wet plants.',
            'Cucumber___healthy': 'No cure needed, plant is healthy.',
            'Grape___Black_rot': 'Apply fungicide and prune infected parts. Improve air circulation.',
            'Grape___Esca_(Black_Measles)': 'Remove infected vines and apply fungicide.',
            'Grape___healthy': 'No cure needed, plant is healthy.',
            'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Apply fungicide and improve air circulation.',
            'Orange___Haunglongbing_(Citrus_greening)': 'Remove infected trees and control psyllids.',
            'Peach___Bacterial_spot': 'Apply copper-based fungicide.',
            'Peach___healthy': 'No cure needed, plant is healthy.',
            'Pepper,_bell___Bacterial_spot': 'Apply copper-based fungicide.',
            'Pepper,_bell___healthy': 'No cure needed, plant is healthy.',
            'Potato___Early_blight': 'Apply fungicide and remove infected leaves. Avoid overhead watering.',
            'Potato___healthy': 'No cure needed, plant is healthy.',
            'Potato___Late_blight': 'Apply fungicide and remove infected plants immediately.',
            'Raspberry___healthy': 'No cure needed, plant is healthy.',
            'Soybean___healthy': 'No cure needed, plant is healthy.',
            'Squash___Powdery_mildew': 'Apply sulfur-based fungicide.',
            'Strawberry___healthy': 'No cure needed, plant is healthy.',
            'Strawberry___Leaf_scorch': 'Improve air circulation and apply fungicide.',
            'Tomato___Bacterial_spot': 'Apply copper-based fungicide. Avoid working with wet plants.',
            'Tomato___Early_blight': 'Apply fungicide and remove infected leaves. Mulch around plants to prevent soil splash.',
            'Tomato___healthy': 'No cure needed, plant is healthy.',
            'Tomato___Late_blight': 'Apply fungicide and remove infected plants. Improve air circulation.',
            'Tomato___Leaf_Mold': 'Improve air circulation and apply fungicide.',
            'Tomato___Septoria_leaf_spot': 'Apply fungicide and remove infected leaves.',
            'Tomato___Spider_mites Two-spotted_spider_mite': 'Use insecticidal soap or neem oil.',
            'Tomato___Target_Spot': 'Apply fungicide and remove infected leaves.',
            'Tomato___Tomato_mosaic_virus': 'Remove infected plants and control aphids.',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Control whiteflies and remove infected plants.',
        }

        cure = cure_info.get(predicted_disease, 'Cure information not available. Consult local agricultural extension service.')

        return jsonify({
            'predicted_disease': predicted_disease,
            'cure_info': cure,
            'confidence': round(confidence * 100, 2),
            'model_used': model_used,
            'image_processed': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def intelligent_crop_prediction(features):
    """Intelligent crop prediction based on soil and climate parameters"""
    N, P, K, temp, humidity, ph, rainfall = features

    crops = {
        'Rice': {'temp': (20, 35), 'rainfall': (150, 300), 'ph': (5.5, 7.0), 'humidity': (60, 90)},
        'Wheat': {'temp': (15, 25), 'rainfall': (50, 100), 'ph': (6.0, 7.5), 'humidity': (40, 70)},
        'Maize': {'temp': (20, 30), 'rainfall': (60, 120), 'ph': (5.5, 7.5), 'humidity': (50, 80)},
        'Cotton': {'temp': (20, 35), 'rainfall': (50, 100), 'ph': (6.0, 8.0), 'humidity': (40, 70)},
        'Sugarcane': {'temp': (20, 35), 'rainfall': (150, 250), 'ph': (6.0, 7.5), 'humidity': (60, 80)},
        'Soybean': {'temp': (20, 30), 'rainfall': (60, 120), 'ph': (6.0, 7.0), 'humidity': (50, 75)},
        'Barley': {'temp': (10, 25), 'rainfall': (40, 80), 'ph': (6.0, 8.0), 'humidity': (40, 70)}
    }

    scores = {}
    for crop, requirements in crops.items():
        score = 0
        # Temperature score
        if requirements['temp'][0] <= temp <= requirements['temp'][1]:
            score += 25
        # Rainfall score
        if requirements['rainfall'][0] <= rainfall <= requirements['rainfall'][1]:
            score += 25
        # pH score
        if requirements['ph'][0] <= ph <= requirements['ph'][1]:
            score += 25
        # Humidity score
        if requirements['humidity'][0] <= humidity <= requirements['humidity'][1]:
            score += 25

        scores[crop] = score

    # Get best crop and alternatives
    sorted_crops = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_crop = sorted_crops[0][0]
    confidence = min(95, sorted_crops[0][1] + 20)  # Add some base confidence

    alternatives = []
    for crop, score in sorted_crops[1:3]:
        alternatives.append({'crop': crop, 'confidence': min(90, score + 15)})

    return best_crop, confidence, alternatives

def get_location_based_recommendations(lat, lon, features):
    """Get location-specific crop recommendations"""
    recommendations = {}

    # Andhra Pradesh (Prakasam district) specific recommendations
    if 15.0 <= lat <= 16.5 and 78.0 <= lon <= 81.0:  # Approximate Andhra Pradesh bounds
        recommendations = {
            'region': 'Prakasam District, Andhra Pradesh',
            'recommended_crops': ['Cotton', 'Chili', 'Rice', 'Groundnut'],
            'seasonal_advice': 'Kharif season: Rice, Cotton; Rabi season: Wheat, Mustard',
            'soil_type': 'Red sandy loam to black cotton soil',
            'irrigation_advice': 'Tank irrigation and borewells are common'
        }

    return recommendations

def enhanced_disease_detection(img):
    """Enhanced disease detection using pattern recognition"""
    try:
        # Identify crop type first
        crop_type = enhanced_identify_crop_type(img)

        # Get disease scores for the identified crop
        disease_scores = calculate_disease_scores(img, crop_type)

        # Find the disease with highest score
        if disease_scores:
            best_disease = max(disease_scores.items(), key=lambda x: x[1])
            predicted_disease = best_disease[0]
            confidence = best_disease[1]
        else:
            predicted_disease = f"{crop_type}___healthy"
            confidence = 0.5

        # If confidence is too low, default to healthy
        if confidence < 0.25:
            predicted_disease = f"{crop_type}___healthy"
            confidence = 0.5

        return predicted_disease, confidence

    except Exception as e:
        print(f"Disease detection error: {e}")
        return "Unknown___healthy", 0.0

def enhanced_identify_crop_type(img):
    """Identify crop type from image using enhanced features and machine learning approach"""
    features = enhanced_analyze_image_features(img)
    crop_scores = {}

    # Debug: print features for analysis
    print(f"Debug - Features: AR={features['aspect_ratio']:.2f}, Circ={features['circularity']:.2f}, Green={features['green_areas']:.2f}, DarkGreen={features['dark_green']:.2f}, Extent={features['extent']:.2f}")

    # Tomato characteristics: Round leaves, compound leaves, medium green
    tomato_score = 0
    if 0.8 <= features['aspect_ratio'] <= 2.2:  # More oval/round leaves
        tomato_score += 0.25
    if features['circularity'] > 0.65:  # Rounder shape
        tomato_score += 0.20
    if 0.35 <= features['green_areas'] <= 0.75:  # Medium green coverage
        tomato_score += 0.25
    if features['dark_green'] > 0.25:  # Good dark green presence
        tomato_score += 0.20
    if features['extent'] > 0.6:  # Leaf fills bounding box well
        tomato_score += 0.10
    crop_scores['Tomato'] = tomato_score

    # Cucumber characteristics: Long, narrow leaves, very elongated
    cucumber_score = 0
    if features['aspect_ratio'] > 2.5:  # Very elongated leaves
        cucumber_score += 0.35
    if features['circularity'] < 0.6:  # Less circular, more elongated
        cucumber_score += 0.25
    if features['green_areas'] > 0.5:  # High green coverage
        cucumber_score += 0.20
    if features['extent'] < 0.7:  # Doesn't fill bounding box as well
        cucumber_score += 0.15
    if features['edges'] > 0.15:  # More complex edge structure
        cucumber_score += 0.05
    crop_scores['Cucumber'] = cucumber_score

    # Potato characteristics: Large, broad leaves, dark green
    potato_score = 0
    if 1.2 <= features['aspect_ratio'] <= 2.0:  # Broad leaves
        potato_score += 0.25
    if features['circularity'] > 0.7:  # Rounder leaves
        potato_score += 0.20
    if features['dark_green'] > 0.4:  # Very dark green
        potato_score += 0.30
    if features['green_areas'] > 0.6:  # High green coverage
        potato_score += 0.20
    if features['extent'] > 0.65:  # Good fill of bounding box
        potato_score += 0.05
    crop_scores['Potato'] = potato_score

    # Corn characteristics: Long, narrow leaves with parallel veins
    corn_score = 0
    if features['aspect_ratio'] > 3.0:  # Very long and narrow
        corn_score += 0.40
    if features['circularity'] < 0.5:  # Very elongated
        corn_score += 0.25
    if features['green_areas'] > 0.4:  # Good green coverage
        corn_score += 0.20
    if features['extent'] < 0.6:  # Long and narrow shape
        corn_score += 0.10
    if features['contrast'] > 0.3:  # Vein structure creates contrast
        corn_score += 0.05
    crop_scores['Corn_(maize)'] = corn_score

    # Apple characteristics: Rounded leaves, lighter green
    apple_score = 0
    if features['aspect_ratio'] < 1.8:  # More rounded
        apple_score += 0.25
    if features['circularity'] > 0.75:  # Very circular
        apple_score += 0.25
    if features['green_areas'] < 0.5:  # Less dense green
        apple_score += 0.20
    if features['dark_green'] < 0.3:  # Lighter green
        apple_score += 0.20
    if features['extent'] > 0.7:  # Good fill
        apple_score += 0.10
    crop_scores['Apple'] = apple_score

    print(f"Debug - Scores: Tomato={tomato_score:.2f}, Cucumber={cucumber_score:.2f}, Potato={potato_score:.2f}, Corn={corn_score:.2f}, Apple={apple_score:.2f}")

    # Get the crop with highest score and check confidence
    if crop_scores:
        best_crop = max(crop_scores.items(), key=lambda x: x[1])
        second_best = sorted(crop_scores.values(), reverse=True)[1] if len(crop_scores) > 1 else 0

        print(f"Debug - Best: {best_crop[0]} ({best_crop[1]:.2f}), Second: {second_best:.2f}, Margin: {best_crop[1] - second_best:.2f}")

        # Only return if confidence is significantly higher than second best
        confidence_margin = best_crop[1] - second_best
        if best_crop[1] > 0.3 and confidence_margin > 0.15:  # Higher threshold and margin
            return best_crop[0]

    return 'unknown'

def enhanced_analyze_image_features(img):
    """Extract enhanced features from plant image"""
    features = {}

    # Convert to different color spaces
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Color-based features
    # Brown spots detection (common in diseases)
    lower_brown = np.array([5, 50, 50])
    upper_brown = np.array([20, 255, 255])
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    features['brown_spots'] = np.sum(brown_mask > 0) / (img.shape[0] * img.shape[1])

    # Yellow areas detection
    lower_yellow = np.array([20, 50, 50])
    upper_yellow = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    features['yellow_areas'] = np.sum(yellow_mask > 0) / (img.shape[0] * img.shape[1])

    # Green areas detection (healthy plant tissue)
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    features['green_areas'] = np.sum(green_mask > 0) / (img.shape[0] * img.shape[1])

    # Dark green areas (healthy leaves)
    lower_dark_green = np.array([35, 100, 50])
    upper_dark_green = np.array([80, 255, 100])
    dark_green_mask = cv2.inRange(hsv, lower_dark_green, upper_dark_green)
    features['dark_green'] = np.sum(dark_green_mask > 0) / (img.shape[0] * img.shape[1])

    # White fungal growth detection
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    features['white_areas'] = np.sum(white_mask > 0) / (img.shape[0] * img.shape[1])

    # Shape features
    # Find contours
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        perimeter = cv2.arcLength(largest_contour, True)

        # Circularity
        if perimeter > 0:
            features['circularity'] = 4 * np.pi * area / (perimeter * perimeter)
        else:
            features['circularity'] = 0

        # Aspect ratio
        x, y, w, h = cv2.boundingRect(largest_contour)
        if h > 0:
            features['aspect_ratio'] = w / h
        else:
            features['aspect_ratio'] = 0

        # Extent
        rect_area = w * h
        if rect_area > 0:
            features['extent'] = area / rect_area
        else:
            features['extent'] = 0
    else:
        features['circularity'] = 0
        features['aspect_ratio'] = 0
        features['extent'] = 0

    # Texture features
    # Edge detection
    edges = cv2.Canny(gray, 100, 200)
    features['edges'] = np.sum(edges > 0) / (img.shape[0] * img.shape[1])

    # Contrast
    features['contrast'] = gray.std()

    return features

def calculate_disease_scores(img, crop_type):
    """Calculate disease scores based on crop type and image features"""
    features = enhanced_analyze_image_features(img)
    disease_scores = {}

    # Get diseases for this crop
    crop_diseases = get_crop_diseases(crop_type)

    for disease in crop_diseases:
        score = 0

        # Disease-specific scoring
        if 'healthy' in disease:
            # Healthy plants have high green areas, low brown/yellow spots
            score = features['green_areas'] * 0.5 + (1 - features['brown_spots']) * 0.3 + (1 - features['yellow_areas']) * 0.2
        elif 'Bacterial_spot' in disease:
            # Bacterial spots: small brown spots, some yellowing
            score = features['brown_spots'] * 0.4 + features['yellow_areas'] * 0.3 + (1 - features['circularity']) * 0.3
        elif 'Early_blight' in disease:
            # Early blight: brown spots with yellow halos
            score = features['brown_spots'] * 0.5 + features['yellow_areas'] * 0.3 + features['edges'] * 0.2
        elif 'Late_blight' in disease:
            # Late blight: dark brown/black spots, white fungal growth
            score = features['brown_spots'] * 0.4 + features['white_areas'] * 0.4 + (1 - features['green_areas']) * 0.2
        elif 'Leaf_Mold' in disease:
            # Leaf mold: yellow patches, white fungal growth
            score = features['yellow_areas'] * 0.4 + features['white_areas'] * 0.4 + features['edges'] * 0.2
        elif 'Septoria_leaf_spot' in disease:
            # Septoria: small brown spots with yellow borders
            score = features['brown_spots'] * 0.5 + features['yellow_areas'] * 0.3 + (1 - features['circularity']) * 0.2
        elif 'Spider_mites' in disease:
            # Spider mites: yellow stippling, webbing (hard to detect visually)
            score = features['yellow_areas'] * 0.6 + (1 - features['green_areas']) * 0.4
        elif 'Target_Spot' in disease:
            # Target spot: concentric brown rings
            score = features['brown_spots'] * 0.5 + features['edges'] * 0.3 + (1 - features['circularity']) * 0.2
        elif 'Powdery_mildew' in disease:
            # Powdery mildew: white powdery coating
            score = features['white_areas'] * 0.7 + (1 - features['green_areas']) * 0.3
        elif 'Downy_mildew' in disease:
            # Downy mildew: yellow patches, white fungal growth underneath
            score = features['yellow_areas'] * 0.4 + features['white_areas'] * 0.4 + (1 - features['green_areas']) * 0.2
        elif 'Angular_leaf_spot' in disease:
            # Angular leaf spot: angular brown spots
            score = features['brown_spots'] * 0.6 + (1 - features['circularity']) * 0.4
        elif 'Bacterial_wilt' in disease:
            # Bacterial wilt: wilting, yellowing
            score = features['yellow_areas'] * 0.6 + (1 - features['green_areas']) * 0.4
        elif 'Apple_scab' in disease:
            # Apple scab: dark spots, olive green
            score = features['brown_spots'] * 0.6 + (1 - features['green_areas']) * 0.4
        elif 'Black_rot' in disease:
            # Black rot: brown/black spots, concentric rings
            score = features['brown_spots'] * 0.7 + features['edges'] * 0.3
        elif 'Cedar_apple_rust' in disease:
            # Cedar apple rust: orange spots
            score = features['yellow_areas'] * 0.5 + features['brown_spots'] * 0.3 + (1 - features['circularity']) * 0.2
        elif 'Common_rust' in disease:
            # Common rust: orange pustules
            score = features['yellow_areas'] * 0.5 + features['brown_spots'] * 0.3 + features['edges'] * 0.2
        elif 'Northern_Leaf_Blight' in disease:
            # Northern leaf blight: long elliptical lesions
            score = features['brown_spots'] * 0.4 + (1 - features['circularity']) * 0.4 + features['aspect_ratio'] * 0.2
        elif 'Cercospora_leaf_spot' in disease:
            # Cercospora leaf spot: gray leaf spot
            score = features['brown_spots'] * 0.5 + features['yellow_areas'] * 0.3 + (1 - features['green_areas']) * 0.2

        # Normalize score to 0-1 range
        disease_scores[disease] = min(1.0, max(0.0, score))

    return disease_scores

def get_crop_diseases(crop_type):
    """Get list of diseases for a specific crop"""
    disease_map = {
        'Tomato': [
            'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___healthy',
            'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
            'Tomato___Tomato_mosaic_virus', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus'
        ],
        'Potato': [
            'Potato___Early_blight', 'Potato___healthy', 'Potato___Late_blight'
        ],
        'Corn_(maize)': [
            'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
            'Corn_(maize)___healthy', 'Corn_(maize)___Northern_Leaf_Blight'
        ],
        'Cucumber': [
            'Cucumber___Powdery_mildew', 'Cucumber___Downy_mildew', 'Cucumber___Bacterial_wilt',
            'Cucumber___Angular_leaf_spot', 'Cucumber___healthy'
        ],
        'Apple': [
            'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy'
        ]
    }

    return disease_map.get(crop_type, ['unknown___healthy'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

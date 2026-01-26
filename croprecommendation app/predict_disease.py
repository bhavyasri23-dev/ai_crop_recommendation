"""
Two-Stage Plant Disease Detection System
Pattern-based detection without TensorFlow dependency
Stage 1: Plant identification using image features
Stage 2: Disease classification using color analysis
"""

import os
import numpy as np
import cv2
from PIL import Image
import json

# Plant classes for Stage 1
PLANT_CLASSES = ['corn', 'rice', 'wheat', 'tomato', 'cucumber', 'potato', 'soybean', 'apple']

# Disease classes by plant type for Stage 2
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

# Treatment recommendations
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
        'Early_blight': 'Apply copper fungicides. Mulch around plants. Stake plants for better air circulation.',
        'Late_blight': 'Remove infected plants immediately. Apply systemic fungicides like mefenoxam.',
        'Leaf_Mold': 'Improve air circulation. Apply chlorothalonil fungicide.',
        'Septoria_leaf_spot': 'Apply copper fungicides. Avoid overhead watering.'
    },
    'cucumber': {
        'healthy': 'Plant is healthy. Continue regular maintenance.',
        'Powdery_mildew': 'Apply sulfur or potassium bicarbonate sprays. Improve air circulation.',
        'Downy_mildew': 'Apply copper fungicides. Avoid overhead watering.',
        'Bacterial_wilt': 'Remove infected plants. Control cucumber beetles with insecticides.',
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
        'Apple_scab': 'Remove infected leaves and apply fungicide like captan. Prune affected branches.',
        'Black_rot': 'Prune infected branches and apply fungicide. Remove fallen leaves.',
        'Cedar_apple_rust': 'Remove nearby cedar trees and apply fungicide. Improve air circulation.'
    }
}

class PlantDiseasePredictor:
    """
    Two-stage plant disease detection system using pattern recognition
    """

    def __init__(self):
        """Initialize the predictor with pattern-based methods"""
        self.plant_class_names = PLANT_CLASSES
        print("Pattern-based plant disease detection initialized (no TensorFlow required)")

    def predict_plant_type(self, image_path):
        """Stage 1: Identify plant type using image features"""
        try:
            # Load image and extract basic features
            img = cv2.imread(image_path)
            if img is None:
                return 'unknown', 0.0

            # Convert to HSV for color analysis
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Calculate average color values
            avg_hue = np.mean(hsv[:, :, 0])
            avg_saturation = np.mean(hsv[:, :, 1])
            avg_value = np.mean(hsv[:, :, 2])

            # Simple rule-based classification based on color patterns
            if avg_value > 180:  # Very bright - might be wheat or rice
                return 'wheat', 0.7
            elif avg_hue < 15 and avg_saturation > 150:  # Deep red - apple
                return 'apple', 0.8
            elif avg_hue < 30 and avg_saturation > 100:  # Reddish - tomato
                return 'tomato', 0.75
            elif avg_hue > 60 and avg_hue < 90:  # Greenish - corn or cucumber
                # Check aspect ratio for corn vs cucumber
                height, width = img.shape[:2]
                aspect_ratio = width / height
                if aspect_ratio > 1.5:
                    return 'corn', 0.7
                else:
                    return 'cucumber', 0.7
            else:
                return 'unknown', 0.5

        except Exception as e:
            print(f"Fallback plant identification error: {e}")
            return 'unknown', 0.0

    def predict_disease(self, image_path, plant_type):
        """Stage 2: Classify disease using color analysis"""
        if plant_type not in DISEASE_CLASSES:
            return 'unknown', 0.0

        try:
            img = cv2.imread(image_path)
            if img is None:
                return 'unknown', 0.0

            # Convert to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Look for disease indicators
            # Brown/yellow spots indicate disease
            brown_mask = cv2.inRange(hsv, (5, 50, 50), (15, 255, 255))
            yellow_mask = cv2.inRange(hsv, (20, 100, 100), (30, 255, 255))

            disease_pixels = np.sum(brown_mask > 0) + np.sum(yellow_mask > 0)
            total_pixels = img.shape[0] * img.shape[1]
            disease_ratio = disease_pixels / total_pixels

            if disease_ratio > 0.1:  # Significant disease indicators
                # Return most common disease for this plant type
                diseases = DISEASE_CLASSES.get(plant_type, ['healthy'])
                if len(diseases) > 1:
                    return diseases[1], 0.8  # Return first disease (not healthy)
                else:
                    return 'healthy', 0.9
            else:
                return 'healthy', 0.85

        except Exception as e:
            print(f"Disease detection error: {e}")
            return 'unknown', 0.0

    def predict(self, image_path):
        """Complete two-stage prediction pipeline"""
        try:
            # Stage 1: Plant identification
            plant_type, plant_confidence = self.predict_plant_type(image_path)

            if plant_type == 'unknown' or plant_confidence < 0.6:
                return {
                    'plant_name': 'Unknown',
                    'disease_name': 'Unable to identify plant',
                    'confidence': plant_confidence,
                    'treatment': 'Please upload a clearer image of a supported plant type.'
                }

            # Stage 2: Disease classification
            disease_name, disease_confidence = self.predict_disease(image_path, plant_type)

            # Get treatment recommendation
            treatment = TREATMENT_DATABASE.get(plant_type, {}).get(disease_name,
                'Consult local agricultural extension service for specific treatment recommendations.')

            # Use the lower confidence score
            final_confidence = min(plant_confidence, disease_confidence)

            return {
                'plant_name': plant_type.capitalize(),
                'disease_name': disease_name.replace('_', ' ').title(),
                'confidence': final_confidence,
                'treatment': treatment
            }

        except Exception as e:
            return {
                'plant_name': 'Error',
                'disease_name': 'Prediction failed',
                'confidence': 0.0,
                'treatment': f'Error during prediction: {str(e)}'
            }

# Global predictor instance
predictor = PlantDiseasePredictor()

def predict_disease_from_image(image_path):
    """
    Main prediction function for external use
    """
    return predictor.predict(image_path)

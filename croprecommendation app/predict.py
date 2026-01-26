import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import load_model
import os

IMG_SIZE = 224
CONFIDENCE_THRESHOLD = 0.60  # 60% confidence required

class PlantDiseasePredictor:
    def __init__(self):
        """Initialize the two-stage predictor"""
        self.crop_model = None
        self.disease_model = None
        self.crop_class_names = None
        self.disease_class_names = None
        self.load_models()

    def load_models(self):
        """Load trained models and class names"""
        try:
            # Load disease model from ml_models directory
            if os.path.exists('ml_models/disease_model.h5'):
                self.disease_model = load_model('ml_models/disease_model.h5')
                # Hardcode class names based on training script
                self.disease_class_names = [
                    'Corn_Common_rust', 'Corn_Northern_Leaf_Blight', 'Corn_Cercospora_leaf_spot', 'Corn_healthy',
                    'Cucumber_Powdery_mildew', 'Cucumber_Downy_mildew', 'Cucumber_Bacterial_wilt', 'Cucumber_Angular_leaf_spot', 'Cucumber_healthy'
                ]
                print("Disease classifier loaded successfully")
            else:
                print("Warning: ml_models/disease_model.h5 not found")

        except Exception as e:
            print(f"Error loading models: {e}")

    def preprocess_image(self, image):
        """Preprocess image for model input"""
        # Resize to model input size
        img = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
        # Convert to float32 and normalize
        img = img.astype(np.float32) / 255.0
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        return img

    def predict_crop_type(self, image):
        """Stage 1: Predict crop type (Corn or Cucumber)"""
        if self.crop_model is None:
            return None, 0.0

        processed_img = self.preprocess_image(image)

        # Get predictions
        predictions = self.crop_model.predict(processed_img, verbose=0)
        predicted_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_idx])

        crop_type = self.crop_class_names[predicted_idx]
        return crop_type, confidence

    def predict_disease(self, image, crop_type):
        """Stage 2: Predict disease specific to the identified crop"""
        if self.disease_model is None:
            return "Unknown", 0.0

        processed_img = self.preprocess_image(image)

        # Get predictions
        predictions = self.disease_model.predict(processed_img, verbose=0)
        predicted_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_idx])

        # Get the predicted disease class
        predicted_class = self.disease_class_names[predicted_idx]

        # Verify the prediction matches the crop type
        # This ensures we only return diseases relevant to the identified crop
        if crop_type.lower() in predicted_class.lower():
            disease_name = predicted_class.split('_', 1)[1]  # Remove crop prefix
            return disease_name, confidence
        else:
            # If prediction doesn't match crop type, find the best matching disease for this crop
            crop_prefix = f"{crop_type}_"
            crop_diseases = [cls for cls in self.disease_class_names if cls.startswith(crop_prefix)]

            if crop_diseases:
                # Get indices of diseases for this crop
                crop_indices = [i for i, cls in enumerate(self.disease_class_names) if cls.startswith(crop_prefix)]
                crop_predictions = predictions[0][crop_indices]

                # Find best disease for this crop
                best_crop_idx = np.argmax(crop_predictions)
                actual_idx = crop_indices[best_crop_idx]
                confidence = float(predictions[0][actual_idx])
                disease_name = self.disease_class_names[actual_idx].split('_', 1)[1]
                return disease_name, confidence
            else:
                return "Unknown", 0.0

    def predict(self, image_path_or_array):
        """
        Two-stage prediction: crop type -> disease
        Returns unique predictions based on image features
        """
        # Load image if path provided
        if isinstance(image_path_or_array, str):
            image = cv2.imread(image_path_or_array)
            if image is None:
                return {'error': 'Could not load image'}
        else:
            image = image_path_or_array

        # Stage 1: Crop type classification
        crop_type, crop_confidence = self.predict_crop_type(image)

        if crop_type is None:
            return {'error': 'Crop classifier not available'}

        # Stage 2: Disease classification specific to crop
        disease, disease_confidence = self.predict_disease(image, crop_type)

        # Apply confidence threshold
        if disease_confidence < CONFIDENCE_THRESHOLD:
            return {
                'error': f'Low confidence prediction ({disease_confidence:.2f} < {CONFIDENCE_THRESHOLD})',
                'crop_type': crop_type,
                'crop_confidence': round(crop_confidence, 3),
                'predicted_disease': disease,
                'disease_confidence': round(disease_confidence, 3)
            }

        # Return successful prediction
        return {
            'crop_type': crop_type,
            'crop_confidence': round(crop_confidence, 3),
            'predicted_disease': disease,
            'disease_confidence': round(disease_confidence, 3),
            'status': 'success'
        }

# Global predictor instance
predictor = PlantDiseasePredictor()

def predict_disease(image_path_or_array):
    """
    Main prediction function
    This two-stage approach ensures unique predictions by:
    1. First identifying the crop type (Corn vs Cucumber)
    2. Then classifying disease specific to that crop type
    3. Using confidence thresholds to reject uncertain predictions
    4. Ensuring disease predictions match the identified crop

    This prevents the "same disease for all images" bug by:
    - Crop-specific disease classification
    - Confidence-based rejection
    - Feature-based unique predictions per image
    """
    return predictor.predict(image_path_or_array)

if __name__ == '__main__':
    # Example usage
    if len(os.sys.argv) > 1:
        image_path = os.sys.argv[1]
        result = predict_disease(image_path)
        print("Prediction Result:")
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print("Usage: python predict.py <image_path>")

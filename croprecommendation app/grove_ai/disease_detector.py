"""
Disease Detector Module for Grove AI

Detects plant diseases using deep learning models specific to each plant type.
"""

import numpy as np
import logging
from .model_loader import ModelLoader
from .image_preprocessing import ImagePreprocessor

logger = logging.getLogger(__name__)

class DiseaseDetector:
    """
    Detects plant diseases from leaf images using plant-specific models.
    """

    def __init__(self, confidence_threshold=0.7):
        """
        Initialize the disease detector.

        Args:
            confidence_threshold (float): Minimum confidence for reliable predictions
        """
        self.confidence_threshold = confidence_threshold
        self.model_loader = ModelLoader()
        self.preprocessor = ImagePreprocessor()
        self.logger = logging.getLogger(__name__)

        # Cache for loaded models
        self.loaded_models = {}

    def detect_disease(self, image_data, plant_type):
        """
        Detect disease in the plant image.

        Args:
            image_data (bytes): Raw image bytes
            plant_type (str): Type of plant ('tomato', 'potato', etc.)

        Returns:
            dict: Disease detection result with disease name and confidence
        """
        try:
            # Validate plant type
            if not self.model_loader.get_supported_plants():
                self.model_loader.load_models()

            if plant_type not in self.model_loader.get_supported_plants():
                return {
                    'disease': 'unknown',
                    'confidence': 0.0,
                    'error': f"Unsupported plant type: {plant_type}",
                    'plant_type': plant_type
                }

            # Validate image
            is_valid, error_msg = self.preprocessor.validate_image(image_data)
            if not is_valid:
                return {
                    'disease': 'unknown',
                    'confidence': 0.0,
                    'error': error_msg,
                    'plant_type': plant_type
                }

            # Get or load disease detection model for this plant
            if plant_type not in self.loaded_models:
                self.loaded_models[plant_type] = self.model_loader.get_disease_detector(plant_type)

            model = self.loaded_models[plant_type]

            # Preprocess image for model
            processed_image = self.preprocessor.preprocess_for_model(image_data)

            # Make prediction
            predictions = model.predict(processed_image, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])

            # Get disease classes for this plant
            disease_classes = self.model_loader.get_disease_classes(plant_type)
            predicted_disease = disease_classes[predicted_class_idx]

            # Check confidence threshold
            if confidence < self.confidence_threshold:
                self.logger.warning(f"Low confidence disease prediction: {predicted_disease} ({confidence:.2f})")
                predicted_disease = 'uncertain'

            result = {
                'disease': predicted_disease,
                'confidence': confidence,
                'plant_type': plant_type,
                'all_predictions': {
                    disease_classes[i]: float(predictions[0][i])
                    for i in range(len(disease_classes))
                }
            }

            self.logger.info(f"Disease detection for {plant_type}: {predicted_disease} (confidence: {confidence:.2f})")
            return result

        except Exception as e:
            self.logger.error(f"Disease detection failed: {str(e)}")
            return {
                'disease': 'unknown',
                'confidence': 0.0,
                'error': f"Detection failed: {str(e)}",
                'plant_type': plant_type
            }

    def get_supported_diseases(self, plant_type):
        """
        Get list of diseases that can be detected for a specific plant type.

        Args:
            plant_type (str): Type of plant

        Returns:
            list: List of disease names or None if plant not supported
        """
        try:
            return self.model_loader.get_disease_classes(plant_type)
        except ValueError:
            return None

    def set_confidence_threshold(self, threshold):
        """
        Set the confidence threshold for predictions.

        Args:
            threshold (float): New confidence threshold (0.0 to 1.0)
        """
        if 0.0 <= threshold <= 1.0:
            self.confidence_threshold = threshold
            self.logger.info(f"Confidence threshold set to {threshold}")
        else:
            raise ValueError("Confidence threshold must be between 0.0 and 1.0")

    def clear_model_cache(self):
        """
        Clear cached models to free memory.
        """
        self.loaded_models.clear()
        self.logger.info("Model cache cleared")

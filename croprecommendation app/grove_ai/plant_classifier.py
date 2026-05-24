"""
Plant Classifier Module for Grove AI

Classifies plant types from leaf images using deep learning models.
"""

import numpy as np
import logging
from .model_loader import ModelLoader
from .image_preprocessing import ImagePreprocessor

logger = logging.getLogger(__name__)

class PlantClassifier:
    """
    Classifies plant types from leaf images using pretrained models.
    """

    def __init__(self, confidence_threshold=0.7):
        """
        Initialize the plant classifier.

        Args:
            confidence_threshold (float): Minimum confidence for reliable predictions
        """
        self.confidence_threshold = confidence_threshold
        self.model_loader = ModelLoader()
        self.preprocessor = ImagePreprocessor()
        self.logger = logging.getLogger(__name__)

        # Cache for loaded model
        self.plant_model = None

    def classify_plant(self, image_data):
        """
        Classify the type of plant from the leaf image.

        Args:
            image_data (bytes): Raw image bytes

        Returns:
            dict: Classification result with plant type and confidence
        """
        try:
            # Validate image
            is_valid, error_msg = self.preprocessor.validate_image(image_data)
            if not is_valid:
                return {
                    'plant_type': 'unknown',
                    'confidence': 0.0,
                    'error': error_msg,
                    'supported_plants': self.model_loader.get_supported_plants()
                }

            # Get or load plant classification model
            if self.plant_model is None:
                self.plant_model = self.model_loader.get_plant_classifier()

            # Preprocess image for model
            processed_image = self.preprocessor.preprocess_for_model(image_data)

            # Make prediction
            predictions = self.plant_model.predict(processed_image, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])

            # Get plant classes
            plant_classes = self.model_loader.PLANT_CLASSES
            predicted_plant = plant_classes[predicted_class_idx]

            # Check confidence threshold
            if confidence < self.confidence_threshold:
                self.logger.warning(f"Low confidence plant classification: {predicted_plant} ({confidence:.2f})")
                predicted_plant = 'unknown'

            result = {
                'plant_type': predicted_plant,
                'confidence': confidence,
                'supported_plants': self.model_loader.get_supported_plants(),
                'all_predictions': {
                    plant_classes[i]: float(predictions[0][i])
                    for i in range(len(plant_classes))
                }
            }

            self.logger.info(f"Plant classification: {predicted_plant} (confidence: {confidence:.2f})")
            return result

        except Exception as e:
            self.logger.error(f"Plant classification failed: {str(e)}")
            return {
                'plant_type': 'unknown',
                'confidence': 0.0,
                'error': f"Classification failed: {str(e)}",
                'supported_plants': self.model_loader.get_supported_plants()
            }

    def get_supported_plants(self):
        """
        Get list of supported plant types.

        Returns:
            list: List of supported plant names
        """
        return self.model_loader.get_supported_plants()

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
        Clear cached model to free memory.
        """
        if self.plant_model is not None:
            del self.plant_model
            self.plant_model = None
        self.logger.info("Model cache cleared")

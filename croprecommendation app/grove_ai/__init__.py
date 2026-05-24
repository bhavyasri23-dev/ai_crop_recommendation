"""
Grove AI - AI-based Plant Disease Detection Module

A comprehensive offline plant disease detection system that:
1. Identifies plant types (tomato, potato, rice, maize)
2. Detects diseases using deep learning models
3. Provides treatment recommendations and prevention tips

Usage:
    from grove_ai import GroveAI

    detector = GroveAI()
    result = detector.analyze_plant(image_bytes)
"""

from .plant_classifier import PlantClassifier
from .disease_detector import DiseaseDetector
from .recommender import DiseaseRecommender
from .model_loader import ModelLoader
from .image_preprocessing import ImagePreprocessor

__version__ = "1.0.0"
__author__ = "Grove AI Team"

class GroveAI:
    """
    Main interface for Grove AI plant disease detection system.
    """

    def __init__(self, confidence_threshold=0.7):
        """
        Initialize Grove AI system.

        Args:
            confidence_threshold (float): Minimum confidence for reliable predictions
        """
        self.confidence_threshold = confidence_threshold

        # Initialize components
        self.plant_classifier = PlantClassifier(confidence_threshold)
        self.disease_detector = DiseaseDetector(confidence_threshold)
        self.recommender = DiseaseRecommender()

    def analyze_plant(self, image_data):
        """
        Complete plant analysis: classify plant type and detect diseases.

        Args:
            image_data (bytes): Raw image bytes of plant leaf

        Returns:
            dict: Complete analysis result
        """
        try:
            # Step 1: Classify plant type
            plant_result = self.plant_classifier.classify_plant(image_data)

            if plant_result['plant_type'] == 'unknown':
                return {
                    'success': False,
                    'error': 'Unable to identify plant type. Please ensure the image shows a clear leaf from a supported plant.',
                    'supported_plants': plant_result['supported_plants'],
                    'plant_classification': plant_result
                }

            plant_type = plant_result['plant_type']

            # Step 2: Detect disease
            disease_result = self.disease_detector.detect_disease(image_data, plant_type)

            # Step 3: Get recommendations
            recommendations = self.recommender.get_recommendations(plant_type, disease_result['disease'])

            # Compile final result
            result = {
                'success': True,
                'plant_type': plant_type,
                'plant_confidence': plant_result['confidence'],
                'disease': disease_result['disease'],
                'disease_confidence': disease_result['confidence'],
                'recommendations': recommendations,
                'details': {
                    'plant_classification': plant_result,
                    'disease_detection': disease_result
                }
            }

            return result

        except Exception as e:
            return {
                'success': False,
                'error': f'Analysis failed: {str(e)}'
            }

    def get_supported_plants(self):
        """
        Get list of supported plant types.

        Returns:
            list: Supported plant names
        """
        return self.plant_classifier.get_supported_plants()

    def get_supported_diseases(self, plant_type):
        """
        Get diseases that can be detected for a specific plant type.

        Args:
            plant_type (str): Type of plant

        Returns:
            list: List of disease names or None if plant not supported
        """
        return self.disease_detector.get_supported_diseases(plant_type)

    def set_confidence_threshold(self, threshold):
        """
        Set confidence threshold for all components.

        Args:
            threshold (float): New confidence threshold (0.0 to 1.0)
        """
        self.confidence_threshold = threshold
        self.plant_classifier.set_confidence_threshold(threshold)
        self.disease_detector.set_confidence_threshold(threshold)

    def cleanup(self):
        """
        Clean up resources and cached models.
        """
        try:
            self.plant_classifier.clear_model_cache()
            self.disease_detector.clear_model_cache()
        except Exception:
            pass

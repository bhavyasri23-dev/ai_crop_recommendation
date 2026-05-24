"""
Model Loader Module for Grove AI

Handles loading and management of pretrained models for plant classification and disease detection.
"""

import os
import tensorflow as tf
import logging
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import numpy as np

logger = logging.getLogger(__name__)

class ModelLoader:
    """
    Loads and manages pretrained models for plant disease detection.
    """

    # Supported plant types
    SUPPORTED_PLANTS = ['tomato', 'potato', 'rice', 'maize']

    # Plant classification classes
    PLANT_CLASSES = SUPPORTED_PLANTS + ['unknown']

    # Disease classes for each plant (simplified for demo)
    DISEASE_CLASSES = {
        'tomato': ['healthy', 'bacterial_spot', 'early_blight', 'late_blight', 'leaf_mold', 'septoria_leaf_spot', 'spider_mites', 'target_spot', 'yellow_leaf_curl_virus', 'mosaic_virus'],
        'potato': ['healthy', 'early_blight', 'late_blight', 'pests'],
        'rice': ['healthy', 'bacterial_leaf_blight', 'brown_spot', 'leaf_smut'],
        'maize': ['healthy', 'common_rust', 'gray_leaf_spot', 'northern_leaf_blight']
    }

    def __init__(self, models_dir='models'):
        """
        Initialize the model loader.

        Args:
            models_dir (str): Directory containing saved models
        """
        self.models_dir = models_dir
        self.plant_classifier = None
        self.disease_detectors = {}
        self.logger = logging.getLogger(__name__)

        # Ensure TensorFlow uses CPU if no GPU available (for compatibility)
        tf.config.set_visible_devices([], 'GPU')

    def create_plant_classifier(self):
        """
        Create and compile plant classification model using EfficientNetB0.

        Returns:
            tf.keras.Model: Compiled plant classification model
        """
        try:
            # Load EfficientNetB0 base model
            base_model = EfficientNetB0(
                weights='imagenet',
                include_top=False,
                input_shape=(224, 224, 3)
            )

            # Freeze base model layers
            base_model.trainable = False

            # Add custom classification head
            x = base_model.output
            x = GlobalAveragePooling2D()(x)
            x = Dense(512, activation='relu')(x)
            x = Dropout(0.3)(x)
            x = Dense(256, activation='relu')(x)
            x = Dropout(0.2)(x)
            predictions = Dense(len(self.PLANT_CLASSES), activation='softmax')(x)

            # Create model
            model = Model(inputs=base_model.input, outputs=predictions)

            # Compile model
            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )

            self.logger.info("Plant classifier model created successfully")
            return model

        except Exception as e:
            self.logger.error(f"Failed to create plant classifier: {str(e)}")
            raise

    def create_disease_detector(self, plant_type):
        """
        Create disease detection model for specific plant type.

        Args:
            plant_type (str): Type of plant ('tomato', 'potato', etc.)

        Returns:
            tf.keras.Model: Compiled disease detection model
        """
        try:
            if plant_type not in self.SUPPORTED_PLANTS:
                raise ValueError(f"Unsupported plant type: {plant_type}")

            disease_classes = self.DISEASE_CLASSES[plant_type]

            # Load EfficientNetB0 base model
            base_model = EfficientNetB0(
                weights='imagenet',
                include_top=False,
                input_shape=(224, 224, 3)
            )

            # Freeze base model layers
            base_model.trainable = False

            # Add custom classification head
            x = base_model.output
            x = GlobalAveragePooling2D()(x)
            x = Dense(512, activation='relu')(x)
            x = Dropout(0.3)(x)
            x = Dense(256, activation='relu')(x)
            x = Dropout(0.2)(x)
            predictions = Dense(len(disease_classes), activation='softmax')(x)

            # Create model
            model = Model(inputs=base_model.input, outputs=predictions)

            # Compile model
            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )

            self.logger.info(f"Disease detector for {plant_type} created successfully")
            return model

        except Exception as e:
            self.logger.error(f"Failed to create disease detector for {plant_type}: {str(e)}")
            raise

    def load_models(self):
        """
        Load or create all required models.

        Returns:
            bool: True if all models loaded successfully
        """
        try:
            # Create plant classifier
            self.plant_classifier = self.create_plant_classifier()

            # Create disease detectors for each supported plant
            for plant in self.SUPPORTED_PLANTS:
                self.disease_detectors[plant] = self.create_disease_detector(plant)

            self.logger.info("All models loaded successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to load models: {str(e)}")
            return False

    def get_plant_classifier(self):
        """
        Get the plant classification model.

        Returns:
            tf.keras.Model: Plant classifier model
        """
        if self.plant_classifier is None:
            self.plant_classifier = self.create_plant_classifier()
        return self.plant_classifier

    def get_disease_detector(self, plant_type):
        """
        Get the disease detection model for specific plant type.

        Args:
            plant_type (str): Type of plant

        Returns:
            tf.keras.Model: Disease detector model
        """
        if plant_type not in self.disease_detectors:
            if plant_type in self.SUPPORTED_PLANTS:
                self.disease_detectors[plant_type] = self.create_disease_detector(plant_type)
            else:
                raise ValueError(f"Unsupported plant type: {plant_type}")

        return self.disease_detectors[plant_type]

    def get_supported_plants(self):
        """
        Get list of supported plant types.

        Returns:
            list: List of supported plant names
        """
        return self.SUPPORTED_PLANTS.copy()

    def get_disease_classes(self, plant_type):
        """
        Get disease classes for specific plant type.

        Args:
            plant_type (str): Type of plant

        Returns:
            list: List of disease class names
        """
        if plant_type not in self.DISEASE_CLASSES:
            raise ValueError(f"Unsupported plant type: {plant_type}")
        return self.DISEASE_CLASSES[plant_type].copy()

    def cleanup(self):
        """
        Clean up TensorFlow resources.
        """
        try:
            if self.plant_classifier is not None:
                del self.plant_classifier

            for detector in self.disease_detectors.values():
                if detector is not None:
                    del detector

            self.disease_detectors.clear()
            tf.keras.backend.clear_session()

            self.logger.info("Model cleanup completed")

        except Exception as e:
            self.logger.warning(f"Model cleanup failed: {str(e)}")

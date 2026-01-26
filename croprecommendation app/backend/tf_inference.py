import tensorflow as tf
import numpy as np
import cv2
from typing import Tuple, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class PlantDiseaseInference:
    """
    TensorFlow inference engine for PlantVillage dataset disease detection.
    Implements two-stage approach: Stage 1 (Crop Detection) and Stage 2 (Disease Detection).
    """

    def __init__(self, model_path: str, class_names_path: str):
        """
        Initialize the inference engine.

        Args:
            model_path: Path to the TensorFlow model (.h5 file)
            class_names_path: Path to the class names text file
        """
        self.model = None
        self.class_names = []
        self.crop_to_diseases = {}
        self.disease_to_crops = {}

        self._load_model(model_path)
        self._load_class_names(class_names_path)
        self._build_crop_disease_mappings()

    def _load_model(self, model_path: str) -> None:
        """Load the TensorFlow model."""
        try:
            self.model = tf.keras.models.load_model(model_path)
            logger.info(f"Successfully loaded model from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def _load_class_names(self, class_names_path: str) -> None:
        """Load class names from text file."""
        try:
            with open(class_names_path, 'r') as f:
                self.class_names = [line.strip() for line in f.readlines() if line.strip()]
            logger.info(f"Loaded {len(self.class_names)} class names")
        except Exception as e:
            logger.error(f"Failed to load class names: {e}")
            raise

    def _build_crop_disease_mappings(self) -> None:
        """Build mappings between crops and diseases for two-stage inference."""
        for class_name in self.class_names:
            if '___' in class_name:
                crop, disease = class_name.split('___', 1)
                crop = crop.strip()
                disease = disease.strip()

                # Map crop to its diseases
                if crop not in self.crop_to_diseases:
                    self.crop_to_diseases[crop] = []
                self.crop_to_diseases[crop].append(disease)

                # Map disease to its crops
                if disease not in self.disease_to_crops:
                    self.disease_to_crops[disease] = []
                self.disease_to_crops[disease].append(crop)

        logger.info(f"Built mappings for {len(self.crop_to_diseases)} crops and {len(self.disease_to_crops)} diseases")

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for model inference.

        Args:
            image: Input image as numpy array (BGR format)

        Returns:
            Preprocessed image ready for model input
        """
        # Convert BGR to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize to model input size (assuming 224x224)
        image = cv2.resize(image, (224, 224))

        # Apply CLAHE for better contrast
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        image = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

        # Gaussian blur to reduce noise
        image = cv2.GaussianBlur(image, (3, 3), 0)

        # Normalize to [0, 1]
        image = image.astype(np.float32) / 255.0

        # Add batch dimension
        image = np.expand_dims(image, axis=0)

        return image

    def predict_class(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Stage 1 & 2 Combined: Predict the full class label.

        Args:
            image: Preprocessed image

        Returns:
            Tuple of (predicted_class, confidence)
        """
        if self.model is None:
            raise ValueError("Model not loaded")

        # Get model predictions
        predictions = self.model.predict(image, verbose=0)
        predicted_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_idx])

        predicted_class = self.class_names[predicted_idx]

        return predicted_class, confidence

    def extract_crop_and_disease(self, class_label: str) -> Tuple[str, str]:
        """
        Extract crop name and disease name from class label.

        Args:
            class_label: Class label in format "Crop___Disease"

        Returns:
            Tuple of (crop_name, disease_name)
        """
        if '___' not in class_label:
            # Handle case where it's just a crop or disease name
            return class_label, "healthy"

        crop, disease = class_label.split('___', 1)
        return crop.strip(), disease.strip()

    def stage1_crop_detection(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Stage 1: Detect the crop type from the image.

        Args:
            image: Preprocessed image

        Returns:
            Tuple of (detected_crop, confidence)
        """
        predicted_class, confidence = self.predict_class(image)
        crop, _ = self.extract_crop_and_disease(predicted_class)
        return crop, confidence

    def stage2_disease_detection(self, image: np.ndarray, crop_context: Optional[str] = None) -> Tuple[str, float]:
        """
        Stage 2: Detect the disease given the crop context.

        Args:
            image: Preprocessed image
            crop_context: Known crop type (optional, for filtering predictions)

        Returns:
            Tuple of (detected_disease, confidence)
        """
        predicted_class, confidence = self.predict_class(image)
        crop, disease = self.extract_crop_and_disease(predicted_class)

        # If crop context is provided and doesn't match, use fallback
        if crop_context and crop != crop_context:
            logger.warning(f"Predicted crop '{crop}' doesn't match context '{crop_context}'")
            # Could implement logic to find best disease for the given crop context
            # For now, return the predicted disease with reduced confidence
            confidence *= 0.8

        return disease, confidence

    def predict_full(self, image: np.ndarray) -> Dict:
        """
        Complete two-stage prediction pipeline.

        Args:
            image: Raw input image (BGR format)

        Returns:
            Dictionary with prediction results
        """
        # Preprocess image
        processed_image = self.preprocess_image(image)

        # Stage 1: Crop Detection
        crop, crop_confidence = self.stage1_crop_detection(processed_image)

        # Stage 2: Disease Detection (using crop context)
        disease, disease_confidence = self.stage2_disease_detection(processed_image, crop)

        # Get full class label
        full_class, full_confidence = self.predict_class(processed_image)

        return {
            'stage1_crop': crop,
            'stage1_confidence': crop_confidence,
            'stage2_disease': disease,
            'stage2_confidence': disease_confidence,
            'full_class': full_class,
            'full_confidence': full_confidence,
            'crop_diseases_available': self.crop_to_diseases.get(crop, [])
        }

    def get_available_crops(self) -> list:
        """Get list of all available crops."""
        return list(self.crop_to_diseases.keys())

    def get_diseases_for_crop(self, crop: str) -> list:
        """Get list of diseases for a specific crop."""
        return self.crop_to_diseases.get(crop, [])

    def get_crops_for_disease(self, disease: str) -> list:
        """Get list of crops that can have a specific disease."""
        return self.disease_to_crops.get(disease, [])


def create_inference_engine(model_path: str = '../ml_models/disease_model.h5',
                          class_names_path: str = '../datasets/processed_images/class_names.txt') -> PlantDiseaseInference:
    """
    Factory function to create and initialize the inference engine.

    Args:
        model_path: Path to the TensorFlow model
        class_names_path: Path to the class names file

    Returns:
        Initialized PlantDiseaseInference instance
    """
    return PlantDiseaseInference(model_path, class_names_path)


# Example usage
if __name__ == "__main__":
    # Initialize the inference engine
    inference_engine = create_inference_engine()

    # Example: Load and predict on an image
    # image = cv2.imread('path/to/image.jpg')
    # results = inference_engine.predict_full(image)
    # print(f"Crop: {results['stage1_crop']} ({results['stage1_confidence']:.2%})")
    # print(f"Disease: {results['stage2_disease']} ({results['stage2_confidence']:.2%})")

    print("Available crops:", inference_engine.get_available_crops())
    print("TensorFlow inference engine initialized successfully!")

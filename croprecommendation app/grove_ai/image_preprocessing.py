"""
Image Preprocessing Module for Grove AI

Handles image loading, validation, and preprocessing for plant disease detection.
"""

import cv2
import numpy as np
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

class ImagePreprocessor:
    """
    Handles image preprocessing for plant disease detection models.
    """

    def __init__(self, target_size=(224, 224)):
        """
        Initialize the image preprocessor.

        Args:
            target_size (tuple): Target size for model input (height, width)
        """
        self.target_size = target_size
        self.logger = logging.getLogger(__name__)

    def load_image(self, image_data):
        """
        Load image from bytes data.

        Args:
            image_data (bytes): Raw image bytes

        Returns:
            np.ndarray: Loaded image array or None if failed
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))

            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Convert to numpy array
            img_array = np.array(image)

            self.logger.info(f"Image loaded successfully. Shape: {img_array.shape}")
            return img_array

        except Exception as e:
            self.logger.error(f"Failed to load image: {str(e)}")
            return None

    def validate_image(self, image_data):
        """
        Validate image data and check if it's suitable for processing.

        Args:
            image_data (bytes): Raw image bytes

        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Check if data exists
            if not image_data or len(image_data) == 0:
                return False, "Empty image data"

            # Try to load image
            img = self.load_image(image_data)
            if img is None:
                return False, "Invalid image format"

            # Check image dimensions
            height, width = img.shape[:2]
            if height < 50 or width < 50:
                return False, "Image too small (minimum 50x50 pixels)"

            if height > 4096 or width > 4096:
                return False, "Image too large (maximum 4096x4096 pixels)"

            # Check if image appears to be a plant leaf (basic check)
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            # Calculate basic statistics
            mean_brightness = np.mean(gray)
            std_brightness = np.std(gray)

            # Very basic leaf-like image check
            if mean_brightness < 30 or std_brightness < 20:
                self.logger.warning("Image may not be a clear plant leaf image")

            return True, None

        except Exception as e:
            return False, f"Image validation failed: {str(e)}"

    def preprocess_for_model(self, image_data):
        """
        Preprocess image for model input.

        Args:
            image_data (bytes): Raw image bytes

        Returns:
            np.ndarray: Preprocessed image array ready for model input
        """
        try:
            # Load image
            img = self.load_image(image_data)
            if img is None:
                raise ValueError("Failed to load image")

            # Resize image
            img_resized = cv2.resize(img, self.target_size, interpolation=cv2.INTER_LINEAR)

            # Normalize pixel values to [0, 1]
            img_normalized = img_resized.astype(np.float32) / 255.0

            # Add batch dimension
            img_batch = np.expand_dims(img_normalized, axis=0)

            self.logger.info(f"Image preprocessed. Final shape: {img_batch.shape}")
            return img_batch

        except Exception as e:
            self.logger.error(f"Image preprocessing failed: {str(e)}")
            raise

    def enhance_image(self, image_data):
        """
        Apply image enhancement techniques for better disease detection.

        Args:
            image_data (bytes): Raw image bytes

        Returns:
            bytes: Enhanced image data
        """
        try:
            img = self.load_image(image_data)
            if img is None:
                return image_data

            # Convert to LAB color space for better contrast enhancement
            lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)

            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])

            # Convert back to RGB
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

            # Convert back to bytes
            enhanced_pil = Image.fromarray(enhanced)
            output_buffer = io.BytesIO()
            enhanced_pil.save(output_buffer, format='JPEG')
            enhanced_data = output_buffer.getvalue()

            self.logger.info("Image enhancement applied successfully")
            return enhanced_data

        except Exception as e:
            self.logger.warning(f"Image enhancement failed, using original: {str(e)}")
            return image_data

    def extract_features(self, image_data):
        """
        Extract basic features from the image for analysis.

        Args:
            image_data (bytes): Raw image bytes

        Returns:
            dict: Dictionary of extracted features
        """
        try:
            img = self.load_image(image_data)
            if img is None:
                return {}

            # Basic color features
            means = cv2.mean(img)
            features = {
                'mean_r': means[0],
                'mean_g': means[1],
                'mean_b': means[2],
                'brightness': np.mean(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)),
                'contrast': np.std(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)),
                'height': img.shape[0],
                'width': img.shape[1]
            }

            return features

        except Exception as e:
            self.logger.error(f"Feature extraction failed: {str(e)}")
            return {}

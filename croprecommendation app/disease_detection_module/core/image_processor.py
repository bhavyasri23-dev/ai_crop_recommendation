"""
Image Processor for Disease Detection
Handles image preprocessing and validation for single-output disease detection
"""

import cv2
import numpy as np
from typing import Optional, Tuple, Dict
import os

# Suppress OpenCV warnings
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'

class ImageProcessor:
    """
    Processes images for disease detection with consistent preprocessing
    """

    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp']

    def validate_image(self, image_data: bytes) -> Optional[str]:
        """
        Validate image data before processing
        Returns error message if invalid, None if valid
        """
        if not image_data:
            return "No image data provided"

        # Check file size (max 5MB)
        if len(image_data) > 5 * 1024 * 1024:
            return "Image file too large (max 5MB)"

        # Try to decode image with error handling
        try:
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return "Invalid image format or corrupted file"
            
            # Additional validation - check image dimensions
            if img.shape[0] < 10 or img.shape[1] < 10:
                return "Image too small (minimum 10x10 pixels)"
            
            if img.shape[0] > 10000 or img.shape[1] > 10000:
                return "Image too large (maximum 10000x10000 pixels)"
                
        except cv2.error as e:
            return f"OpenCV error processing image: {str(e)}"
        except Exception as e:
            return f"Error processing image: {str(e)}"

        return None

    def preprocess_image(self, image_data: bytes) -> Optional[np.ndarray]:
        """
        Preprocess image for model input
        Returns preprocessed image array or None if processing fails
        """
        try:
            # Decode image
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                return None

            # Resize to target size
            img = cv2.resize(img, self.target_size)

            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Normalize pixel values to [0, 1]
            img = img.astype(np.float32) / 255.0

            # Add batch dimension
            img = np.expand_dims(img, axis=0)

            return img

        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None

    def extract_image_features(self, image_data: bytes) -> Optional[Dict]:
        """
        Extract advanced features from image including GLCM, FFT, and enhanced color analysis
        """
        try:
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                return None

            # Basic image properties
            height, width, channels = img.shape
            file_size = len(image_data)

            # Color analysis in multiple color spaces
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Calculate basic statistics
            brightness = np.mean(gray)
            contrast = gray.std()
            saturation = np.mean(hsv[:, :, 1])

            # Edge detection for texture analysis
            edges = cv2.Canny(gray, 100, 200)
            edge_density = np.sum(edges > 0) / (height * width)

            # GLCM (Gray Level Co-occurrence Matrix) features
            glcm_features = self._extract_glcm_features(gray)

            # FFT analysis for frequency domain features
            fft_features = self._extract_fft_features(gray)

            # Enhanced color features
            color_features = self._extract_color_features(img, hsv, lab)

            # Combine all features
            features = {
                'dimensions': f"{width}x{height}",
                'file_size_kb': file_size / 1024,
                'brightness': float(brightness),
                'contrast': float(contrast),
                'saturation': float(saturation),
                'edge_density': float(edge_density),
                'aspect_ratio': width / height if height > 0 else 0
            }

            # Add GLCM features
            features.update(glcm_features)

            # Add FFT features
            features.update(fft_features)

            # Add color features
            features.update(color_features)

            return features

        except Exception as e:
            print(f"Error extracting image features: {e}")
            return None

    def _extract_glcm_features(self, gray_img: np.ndarray) -> Dict:
        """Extract GLCM texture features"""
        try:
            # Compute GLCM
            glcm = self._compute_glcm(gray_img)

            # Calculate texture features
            contrast = np.sum(glcm * np.arange(glcm.shape[0])[:, None]**2)
            homogeneity = np.sum(glcm / (1 + np.arange(glcm.shape[0])[:, None]**2))
            energy = np.sum(glcm**2)
            entropy = -np.sum(glcm * np.log(glcm + 1e-10))

            return {
                'glcm_contrast': float(contrast),
                'glcm_homogeneity': float(homogeneity),
                'glcm_energy': float(energy),
                'glcm_entropy': float(entropy)
            }
        except Exception as e:
            print(f"Error extracting GLCM features: {e}")
            return {
                'glcm_contrast': 0.0,
                'glcm_homogeneity': 0.0,
                'glcm_energy': 0.0,
                'glcm_entropy': 0.0
            }

    def _compute_glcm(self, gray_img: np.ndarray, distances: list = [1], angles: list = [0]) -> np.ndarray:
        """Compute Gray Level Co-occurrence Matrix"""
        try:
            # Normalize to 0-255 range and convert to uint8
            gray_norm = cv2.normalize(gray_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

            # Reduce to 16 gray levels for GLCM computation
            gray_reduced = (gray_norm // 16).astype(np.uint8)

            # Compute GLCM
            glcm = np.zeros((16, 16), dtype=np.float32)

            height, width = gray_reduced.shape
            for i in range(height - 1):
                for j in range(width - 1):
                    current = gray_reduced[i, j]
                    right = gray_reduced[i, j + 1]
                    glcm[current, right] += 1

            # Normalize GLCM
            glcm = glcm / np.sum(glcm) if np.sum(glcm) > 0 else glcm

            return glcm
        except Exception as e:
            print(f"Error computing GLCM: {e}")
            return np.zeros((16, 16), dtype=np.float32)

    def _extract_fft_features(self, gray_img: np.ndarray) -> Dict:
        """Extract frequency domain features using FFT"""
        try:
            # Compute FFT
            fft = np.fft.fft2(gray_img)
            fft_shift = np.fft.fftshift(fft)
            magnitude_spectrum = 20 * np.log(np.abs(fft_shift) + 1)

            # Extract frequency domain features
            height, width = magnitude_spectrum.shape
            center_h, center_w = height // 2, width // 2

            # High frequency energy (texture indicator)
            high_freq_mask = np.zeros_like(magnitude_spectrum)
            high_freq_mask[center_h//2:3*center_h//2, center_w//2:3*center_w//2] = 1
            high_freq_energy = np.sum(magnitude_spectrum * high_freq_mask)

            # Low frequency energy (smooth areas)
            low_freq_mask = np.ones_like(magnitude_spectrum)
            low_freq_mask[center_h//4:3*center_h//4, center_w//4:3*center_w//4] = 0
            low_freq_energy = np.sum(magnitude_spectrum * low_freq_mask)

            # Frequency ratio
            freq_ratio = high_freq_energy / (low_freq_energy + 1e-10)

            return {
                'fft_high_freq_energy': float(high_freq_energy),
                'fft_low_freq_energy': float(low_freq_energy),
                'fft_freq_ratio': float(freq_ratio)
            }
        except Exception as e:
            print(f"Error extracting FFT features: {e}")
            return {
                'fft_high_freq_energy': 0.0,
                'fft_low_freq_energy': 0.0,
                'fft_freq_ratio': 0.0
            }

    def _extract_color_features(self, img: np.ndarray, hsv: np.ndarray, lab: np.ndarray) -> Dict:
        """Extract advanced color features"""
        try:
            # Color channel statistics
            b, g, r = cv2.split(img)
            l, a, b_lab = cv2.split(lab)
            h, s, v = cv2.split(hsv)

            features = {
                'color_std_r': float(np.std(r)),
                'color_std_g': float(np.std(g)),
                'color_std_b': float(np.std(b)),
                'color_mean_l': float(np.mean(l)),
                'color_std_l': float(np.std(l)),
                'color_mean_a': float(np.mean(a)),
                'color_std_a': float(np.std(a)),
                'color_mean_b_lab': float(np.mean(b_lab)),
                'color_std_b_lab': float(np.std(b_lab))
            }

            # Color diversity (unique colors)
            unique_colors = len(np.unique(img.reshape(-1, img.shape[2]), axis=0))
            features['color_diversity'] = unique_colors / (img.shape[0] * img.shape[1])

            return features
        except Exception as e:
            print(f"Error extracting color features: {e}")
            return {
                'color_std_r': 0.0,
                'color_std_g': 0.0,
                'color_std_b': 0.0,
                'color_mean_l': 0.0,
                'color_std_l': 0.0,
                'color_mean_a': 0.0,
                'color_std_a': 0.0,
                'color_mean_b_lab': 0.0,
                'color_std_b_lab': 0.0,
                'color_diversity': 0.0
            }

    def is_leaf_image(self, image_data: bytes, confidence_threshold: float = 0.1) -> Tuple[bool, float]:
        """
        Very permissive check for any plant material (accepts most images)
        Returns (is_leaf, confidence)
        """
        features = self.extract_image_features(image_data)
        if not features:
            return True, 0.5  # Accept if we can't analyze but image is valid

        # Very permissive heuristics - accept most images
        score = 0.5  # Start with base acceptance

        # Aspect ratio (most images are acceptable)
        if 0.1 <= features['aspect_ratio'] <= 10.0:
            score += 0.2

        # Brightness (very wide range)
        if 10 <= features['brightness'] <= 245:
            score += 0.2

        # Texture (most images have some texture)
        if 0.001 <= features['edge_density'] <= 0.8:
            score += 0.2

        # Green content check (optional bonus)
        try:
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is not None:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                # Count green pixels (hue 35-80 is typically green)
                green_mask = cv2.inRange(hsv, (35, 50, 50), (80, 255, 255))
                green_ratio = np.sum(green_mask > 0) / (img.shape[0] * img.shape[1])
                if green_ratio > 0.01:  # At least 1% green content gives bonus
                    score += 0.1
        except:
            pass  # Skip green check if image processing fails

        return score >= confidence_threshold, score

# Global instance
image_processor = ImageProcessor()


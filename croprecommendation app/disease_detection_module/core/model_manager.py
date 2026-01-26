"""
Model Manager for Disease Detection
Handles loading and managing the CNN model for disease detection
"""

import os
from typing import Optional, Dict, List

# Optional TensorFlow import - only import if available
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
    # Configure TensorFlow to avoid memory and session issues
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass  # Memory growth must be set before GPUs are initialized
    # Set TF_CPP_MIN_LOG_LEVEL to suppress warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available, model manager will be disabled")

class ModelManager:
    """
    Manages the disease detection CNN model
    """

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or os.path.join(
            os.path.dirname(__file__), '..', 'models', 'disease_model.h5'
        )
        self.model = None
        self.model_info = {}
        self.available_models = []
        self._session = None

    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None

    def load_model(self) -> bool:
        """
        Load the disease detection model with proper session handling and validation
        """
        try:
            # Reset default graph to avoid conflicts
            tf.compat.v1.reset_default_graph()

            if os.path.exists(self.model_path):
                # Create a new session for model loading
                self._session = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(
                    allow_soft_placement=True,
                    log_device_placement=False
                ))
                with self._session.as_default():
                    self.model = tf.keras.models.load_model(self.model_path, compile=False)
                    # Recompile with proper metrics
                    self.model.compile(
                        optimizer='adam',
                        loss='categorical_crossentropy',
                        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3)]
                    )
                    self._extract_model_info()
                    self._validate_model()
                print(f"Model loaded successfully from {self.model_path}")
                return True
            else:
                print(f"Model file not found: {self.model_path}")
                return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def _extract_model_info(self):
        """Extract information about the loaded model"""
        if self.model is None:
            return

        try:
            self.model_info = {
                'input_shape': self.model.input_shape,
                'output_shape': self.model.output_shape,
                'layers': len(self.model.layers),
                'trainable_params': sum([layer.count_params() for layer in self.model.layers if layer.trainable]),
                'total_params': self.model.count_params()
            }
        except Exception as e:
            print(f"Error extracting model info: {e}")
            self.model_info = {}

    def _validate_model(self):
        """Validate that the model can make predictions"""
        if self.model is None:
            return False

        try:
            # Create a dummy input to test the model
            dummy_input = tf.random.normal(self.model.input_shape)
            dummy_input = tf.expand_dims(dummy_input, axis=0) if len(self.model.input_shape) == 3 else dummy_input

            # Test prediction
            test_pred = self.model.predict(dummy_input, verbose=0)
            print(f"Model validation successful - output shape: {test_pred.shape}")
            return True
        except Exception as e:
            print(f"Model validation failed: {e}")
            return False

    def get_model_info(self) -> Dict:
        """Get model information"""
        return self.model_info

    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        models_dir = os.path.dirname(self.model_path)
        if os.path.exists(models_dir):
            return [f for f in os.listdir(models_dir) if f.endswith('.h5')]
        return []

    def predict(self, input_data):
        """
        Make prediction using the loaded model with proper session handling
        """
        if not TENSORFLOW_AVAILABLE:
            raise ValueError("TensorFlow not available")

        if self.model is None:
            raise ValueError("Model not loaded")

        try:
            if self._session is not None:
                with self._session.as_default():
                    return self.model.predict(input_data, verbose=0)
            else:
                return self.model.predict(input_data, verbose=0)
        except Exception as e:
            # If session-based prediction fails, try with a fresh session
            print(f"Prediction error, retrying with fresh session: {e}")
            self._session = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(
                allow_soft_placement=True
            ))
            with self._session.as_default():
                return self.model.predict(input_data, verbose=0)

    def close(self):
        """Close the TensorFlow session"""
        if not TENSORFLOW_AVAILABLE:
            return

        if self._session is not None:
            self._session.close()
            self._session = None

# Global instance
model_manager = ModelManager()


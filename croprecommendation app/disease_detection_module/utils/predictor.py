import numpy as np
from tensorflow.keras.models import load_model
from utils.image_utils import preprocess_image, is_leaf_image

disease_model = load_model("models/disease_model.h5")

CLASS_NAMES = [
    "Healthy",
    "Rust",
    "Leaf Spot",
    "Blight",
    "Downy Mildew",
    "Powdery Mildew"
]

CONF_HIGH = 0.75
CONF_MED = 0.50


def predict_disease(img_bytes, crop_type="unknown"):
    # STEP 1: LEAF CHECK
    is_leaf, leaf_conf = is_leaf_image(img_bytes)

    if not is_leaf:
        return {
            "prediction": "Uncertain",
            "reason": "Input image is not a leaf",
            "leaf_confidence": round(leaf_conf, 3)
        }

    # STEP 2: DISEASE MODEL
    img = preprocess_image(img_bytes)
    preds = disease_model.predict(img)[0]

    idx = np.argmax(preds)
    confidence = float(preds[idx])
    label = CLASS_NAMES[idx]

    # STEP 3: CONFIDENCE LOGIC (CRITICAL FIX)
    if confidence >= CONF_HIGH:
        return {
            "prediction": label,
            "confidence": round(confidence, 3),
            "crop": crop_type
        }

    elif CONF_MED <= confidence < CONF_HIGH:
        return {
            "prediction": "Uncertain",
            "reason": "Low disease confidence",
            "top_prediction": label,
            "confidence": round(confidence, 3)
        }

    else:
        return {
            "prediction": "Uncertain",
            "reason": "Image quality insufficient",
            "confidence": round(confidence, 3)
        }

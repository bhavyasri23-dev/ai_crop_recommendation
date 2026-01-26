import cv2
import numpy as np
from tensorflow.keras.models import load_model

leaf_model = load_model("models/leaf_detector.h5")

IMG_SIZE = 224

def preprocess_image(img_bytes):
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    return np.expand_dims(img, axis=0)


def is_leaf_image(img_bytes, threshold=0.7):
    img = preprocess_image(img_bytes)
    prob = leaf_model.predict(img)[0][0]   # binary classifier
    return prob >= threshold, float(prob)

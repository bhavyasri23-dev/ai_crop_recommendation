import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import app
import numpy as np
import io
from PIL import Image

def test_model_loading():
    try:
        from app import crop_model, disease_model, disease_classes
        print("Models loaded successfully.")
        print(f"Disease classes: {len(disease_classes)}")
    except Exception as e:
        print(f"Model loading failed: {e}")
        return False
    return True

def test_predict_crop():
    with app.test_client() as client:
        # Valid data
        data = {
            "N": 10,
            "P": 5,
            "K": 20,
            "temperature": 25,
            "humidity": 50,
            "pH": 6.5,
            "rainfall": 100
        }
        response = client.post('/predict_crop', json=data)
        print(f"Predict crop status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.get_json()}")
        else:
            print(f"Error: {response.get_data(as_text=True)}")

        # Invalid data - missing key
        data_missing = {
            "humidity": 50,
            "N": 10,
            "P": 5,
            "K": 20,
            "temperature": 25,
            "rainfall": 100
        }
        response = client.post('/predict_crop', json=data_missing)
        print(f"Predict crop missing key status: {response.status_code}")
        print(f"Error: {response.get_json()}")

        # Invalid data - wrong type
        data_wrong = {
            "ph": "six",
            "humidity": 50,
            "N": 10,
            "P": 5,
            "K": 20,
            "temperature": 25,
            "rainfall": 100
        }
        response = client.post('/predict_crop', json=data_wrong)
        print(f"Predict crop wrong type status: {response.status_code}")
        print(f"Error: {response.get_json()}")

def test_predict_disease():
    with app.test_client() as client:
        # Load a sample image from processed_images
        try:
            images = np.load('../datasets/processed_images/images.npy')
            sample_img = images[0]  # Take first image
            # Convert numpy array to PIL Image, then to bytes
            img = Image.fromarray((sample_img * 255).astype(np.uint8))
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)

            response = client.post('/predict_disease', data={'image': (img_bytes, 'test.jpg')}, content_type='multipart/form-data')
            print(f"Predict disease status: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.get_json()}")
            else:
                print(f"Error: {response.get_data(as_text=True)}")
        except Exception as e:
            print(f"Failed to load or send image: {e}")

        # Invalid - no file
        response = client.post('/predict_disease')
        print(f"Predict disease no file status: {response.status_code}")
        print(f"Error: {response.get_json()}")

if __name__ == '__main__':
    if test_model_loading():
        test_predict_crop()
        test_predict_disease()
    else:
        print("Cannot proceed with testing due to model loading failure.")

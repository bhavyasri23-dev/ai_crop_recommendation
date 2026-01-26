import os
import cv2
import numpy as np
import zipfile
from sklearn.model_selection import train_test_split

# Extract archive.zip if not already extracted
archive_path = 'datasets/archive.zip'
extract_dir = 'datasets/plant_disease_images'

if not os.path.exists(extract_dir):
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print("Archive extracted.")

# Assuming images are in datasets/plant_disease_images/plantvillage dataset/color/ with subfolders for classes
image_dir = os.path.join(extract_dir, 'plantvillage dataset', 'color')
processed_dir = 'datasets/processed_images/'

if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

def preprocess_image(image_path, target_size=(224, 224)):
    img = cv2.imread(image_path)
    if img is None:
        return None
    img = cv2.resize(img, target_size)
    img = img / 255.0  # Normalize to 0-1
    return img

images = []
labels = []
class_names = os.listdir(image_dir)
for i, class_name in enumerate(class_names):
    class_dir = os.path.join(image_dir, class_name)
    if os.path.isdir(class_dir):
        for img_name in os.listdir(class_dir):
            img_path = os.path.join(class_dir, img_name)
            img = preprocess_image(img_path)
            if img is not None:
                images.append(img)
                labels.append(i)

images = np.array(images)
labels = np.array(labels)

# Save processed data
np.save(os.path.join(processed_dir, 'images.npy'), images)
np.save(os.path.join(processed_dir, 'labels.npy'), labels)
with open(os.path.join(processed_dir, 'class_names.txt'), 'w') as f:
    f.write('\n'.join(class_names))

print("Image data processed.")

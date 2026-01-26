import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.utils.class_weight import compute_class_weight
from sklearn.model_selection import train_test_split
import cv2

# PlantVillage dataset structure: dataset/train/Corn_Common_rust/... etc.
DATASET_PATH = 'dataset'
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 25

# Disease classes for each crop
CORN_DISEASES = ['Common_rust', 'Northern_Leaf_Blight', 'Cercospora_leaf_spot', 'healthy']
CUCUMBER_DISEASES = ['Powdery_mildew', 'Downy_mildew', 'Bacterial_wilt', 'Angular_leaf_spot', 'healthy']

# Combined class names for the model
ALL_CLASSES = CORN_DISEASES + CUCUMBER_DISEASES
CLASS_NAMES = [f'Corn_{d}' for d in CORN_DISEASES] + [f'Cucumber_{d}' for d in CUCUMBER_DISEASES]

def load_disease_data():
    """Load and preprocess disease classification data"""
    X = []
    y = []
    class_to_idx = {name: idx for idx, name in enumerate(CLASS_NAMES)}

    # Load Corn diseases
    for disease in CORN_DISEASES:
        class_path = os.path.join(DATASET_PATH, 'train', f'Corn_{disease}')
        if not os.path.exists(class_path):
            print(f"Warning: {class_path} not found")
            continue

        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = cv2.imread(img_path)
            if img is None:
                continue
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            img = img.astype(np.float32) / 255.0
            X.append(img)
            y.append(class_to_idx[f'Corn_{disease}'])

    # Load Cucumber diseases
    for disease in CUCUMBER_DISEASES:
        class_path = os.path.join(DATASET_PATH, 'train', f'Cucumber_{disease}')
        if not os.path.exists(class_path):
            print(f"Warning: {class_path} not found")
            continue

        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = cv2.imread(img_path)
            if img is None:
                continue
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            img = img.astype(np.float32) / 255.0
            X.append(img)
            y.append(class_to_idx[f'Cucumber_{disease}'])

    X = np.array(X)
    y = np.array(y)

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    return X_train, X_val, y_train, y_val, CLASS_NAMES

def build_disease_model(num_classes):
    """Build EfficientNetB3 model for disease classification"""
    base_model = EfficientNetB3(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))

    # Freeze base model layers initially
    for layer in base_model.layers:
        layer.trainable = False

    # Add custom head with more layers for better disease discrimination
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    return model, base_model

def train_disease_classifier():
    """Train the disease classifier"""
    print("Loading disease data...")
    X_train, X_val, y_train, y_val, class_names = load_disease_data()

    print(f"Training samples: {len(X_train)}, Validation samples: {len(X_val)}")
    print(f"Classes: {class_names}")

    # Compute class weights for imbalance handling
    class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
    class_weight_dict = dict(enumerate(class_weights))

    # Build model
    model, base_model = build_disease_model(len(class_names))

    # Compile
    model.compile(optimizer=Adam(learning_rate=1e-3),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_accuracy', patience=7, restore_best_weights=True),
        ModelCheckpoint('disease_classifier.h5', monitor='val_accuracy', save_best_only=True)
    ]

    # Initial training with frozen base
    print("Initial training...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        class_weight=class_weight_dict,
        callbacks=callbacks
    )

    # Fine-tune: unfreeze more layers for better feature extraction
    print("Fine-tuning...")
    for layer in base_model.layers[-50:]:  # Unfreeze last 50 layers
        layer.trainable = True

    # Lower learning rate for fine-tuning
    model.compile(optimizer=Adam(learning_rate=1e-5),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=15,
        batch_size=BATCH_SIZE,
        class_weight=class_weight_dict,
        callbacks=callbacks
    )

    # Save model and class names
    model.save('disease_classifier.h5')
    np.save('disease_class_names.npy', class_names)

    print("Disease classifier training completed!")

if __name__ == '__main__':
    train_disease_classifier()

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

# PlantVillage dataset structure assumed: dataset/train/Corn/... and dataset/train/Cucumber/...
DATASET_PATH = 'dataset'
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20

def load_data():
    """Load and preprocess data for crop classification"""
    X = []
    y = []
    class_names = ['Corn', 'Cucumber']
    class_to_idx = {name: idx for idx, name in enumerate(class_names)}

    for class_name in class_names:
        class_path = os.path.join(DATASET_PATH, 'train', class_name)
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
            y.append(class_to_idx[class_name])

    X = np.array(X)
    y = np.array(y)

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    return X_train, X_val, y_train, y_val, class_names

def build_model(num_classes):
    """Build EfficientNetB3 model for crop classification"""
    base_model = EfficientNetB3(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))

    # Freeze base model layers
    for layer in base_model.layers:
        layer.trainable = False

    # Add custom head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    return model, base_model

def train_crop_classifier():
    """Train the crop type classifier"""
    print("Loading data...")
    X_train, X_val, y_train, y_val, class_names = load_data()

    print(f"Training samples: {len(X_train)}, Validation samples: {len(X_val)}")

    # Compute class weights for imbalance
    class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
    class_weight_dict = dict(enumerate(class_weights))

    # Build model
    model, base_model = build_model(len(class_names))

    # Compile
    model.compile(optimizer=Adam(learning_rate=1e-3),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # Callbacks
    callbacks = [
        EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True),
        ModelCheckpoint('crop_classifier.h5', monitor='val_accuracy', save_best_only=True)
    ]

    # Train
    print("Training crop classifier...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        class_weight=class_weight_dict,
        callbacks=callbacks
    )

    # Fine-tune: unfreeze top layers
    print("Fine-tuning...")
    for layer in base_model.layers[-20:]:  # Unfreeze last 20 layers
        layer.trainable = True

    model.compile(optimizer=Adam(learning_rate=1e-5),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=10,
        batch_size=BATCH_SIZE,
        class_weight=class_weight_dict,
        callbacks=callbacks
    )

    # Save model and class names
    model.save('crop_classifier.h5')
    np.save('crop_class_names.npy', class_names)

    print("Crop classifier training completed!")

if __name__ == '__main__':
    train_crop_classifier()

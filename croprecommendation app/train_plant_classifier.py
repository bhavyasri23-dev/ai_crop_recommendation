"""
Plant Identification Classifier Training (Stage 1)
Trains a model to identify plant types: corn, rice, wheat, tomato, cucumber, potato, soybean
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

# Plant classes for Stage 1
PLANT_CLASSES = ['corn', 'rice', 'wheat', 'tomato', 'cucumber', 'potato', 'soybean']

def create_data_generators(data_dir, img_size=(224, 224), batch_size=32):
    """
    Create data generators for training and validation
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )

    # Only rescaling for validation
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    # Training generator
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        classes=PLANT_CLASSES,
        subset='training',
        shuffle=True
    )

    # Validation generator
    validation_generator = val_datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        classes=PLANT_CLASSES,
        subset='validation',
        shuffle=False
    )

    return train_generator, validation_generator

def build_plant_classifier_model(num_classes):
    """
    Build EfficientNetB3-based plant identification model
    """
    # Load EfficientNetB3 base model
    base_model = EfficientNetB3(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )

    # Freeze base model layers
    for layer in base_model.layers:
        layer.trainable = False

    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.3)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    # Create model
    model = Model(inputs=base_model.input, outputs=predictions)

    return model, base_model

def fine_tune_model(model, base_model, learning_rate=1e-4):
    """
    Fine-tune the model by unfreezing some layers
    """
    # Unfreeze the last 30 layers of the base model
    for layer in base_model.layers[-30:]:
        layer.trainable = True

    # Compile with lower learning rate for fine-tuning
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

def plot_training_history(history, save_path='plant_classifier_training_history.png'):
    """
    Plot training history
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Accuracy plot
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()

    # Loss plot
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

def train_plant_classifier(data_dir, model_save_path='models/plant_classifier.h5',
                          epochs=50, batch_size=32):
    """
    Main training function for plant classifier
    """
    print("Starting Plant Classifier Training...")
    print(f"Plant classes: {PLANT_CLASSES}")

    # Create data generators
    train_generator, validation_generator = create_data_generators(
        data_dir, batch_size=batch_size
    )

    num_classes = len(PLANT_CLASSES)
    print(f"Number of classes: {num_classes}")

    # Build model
    model, base_model = build_plant_classifier_model(num_classes)

    # Initial training with frozen base
    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Callbacks
    checkpoint = ModelCheckpoint(
        model_save_path,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )

    early_stopping = EarlyStopping(
        monitor='val_accuracy',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )

    reduce_lr = ReduceLROnPlateau(
        monitor='val_accuracy',
        factor=0.2,
        patience=5,
        min_lr=1e-6,
        verbose=1
    )

    # Initial training
    print("\n=== Phase 1: Training with frozen base model ===")
    history1 = model.fit(
        train_generator,
        epochs=epochs//2,
        validation_data=validation_generator,
        callbacks=[checkpoint, early_stopping, reduce_lr],
        verbose=1
    )

    # Fine-tuning
    print("\n=== Phase 2: Fine-tuning with unfrozen layers ===")
    model = fine_tune_model(model, base_model)

    history2 = model.fit(
        train_generator,
        epochs=epochs//2,
        validation_data=validation_generator,
        callbacks=[checkpoint, early_stopping, reduce_lr],
        verbose=1
    )

    # Combine histories
    combined_history = {}
    for key in history1.history.keys():
        combined_history[key] = history1.history[key] + history2.history[key]

    # Save final model
    model.save(model_save_path.replace('.h5', '_final.h5'))
    print(f"\nModel saved to {model_save_path}")

    # Plot training history
    plot_training_history(combined_history)

    # Evaluate final model
    print("\n=== Final Model Evaluation ===")
    loss, accuracy = model.evaluate(validation_generator, verbose=1)
    print(".4f"    print(".4f"
    return model, combined_history

if __name__ == "__main__":
    # Set random seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)

    # Data directory (adjust path as needed)
    data_dir = "datasets/plant_images"  # Should contain subfolders for each plant class

    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)

    # Train the model
    model, history = train_plant_classifier(
        data_dir=data_dir,
        model_save_path='models/plant_classifier.h5',
        epochs=50,
        batch_size=32
    )

    print("\nPlant classifier training completed!")

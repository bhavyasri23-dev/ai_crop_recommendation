import joblib
import numpy as np
import pandas as pd

def test_saved_models():
    try:
        # Load models
        crop_model = joblib.load('../ml_models/crop_model.pkl')
        yield_model = joblib.load('../ml_models/yield_model.pkl')
        profit_model = joblib.load('../ml_models/profit_model.pkl')
        print("Models loaded successfully.")
    except Exception as e:
        print(f"Failed to load models: {e}")
        return

    # Sample data for testing
    sample_data = pd.DataFrame({
        'N': [30, 50, 20],
        'P': [20, 30, 15],
        'K': [20, 40, 10],
        'temperature': [15, 25, 30],
        'humidity': [50, 60, 70],
        'ph': [6.5, 7.0, 5.5],
        'rainfall': [75, 100, 150]
    })

    print("\nTesting predictions on sample data:")
    for i, row in sample_data.iterrows():
        features = row.values.reshape(1, -1)
        crop_pred = crop_model.predict(features)[0]
        yield_pred = yield_model.predict(features)[0]
        profit_pred = profit_model.predict(features)[0]
        print(f"Sample {i+1}: Crop={crop_pred}, Yield={yield_pred:.2f}, Profit={profit_pred:.2f}")

if __name__ == '__main__':
    test_saved_models()

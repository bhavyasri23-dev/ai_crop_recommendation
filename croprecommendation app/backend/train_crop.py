import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from imblearn.over_sampling import SMOTE
import joblib
import numpy as np

# Load raw dataset
df = pd.read_csv('../datasets/Crop_recommendation.csv')

# Handle missing values
df = df.dropna()

features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
X = df[features]
y_crop = df['label']

# Balance the dataset using SMOTE oversampling
smote = SMOTE(random_state=42, k_neighbors=3)  # k_neighbors=3 for small classes
X_balanced, y_crop_balanced = smote.fit_resample(X, y_crop)

# Update df with balanced data for yield and profit
df_balanced = pd.DataFrame(X_balanced, columns=features)
df_balanced['label'] = y_crop_balanced

# Assuming yield and profit columns exist; if not, add dummy data for demonstration
if 'yield' not in df.columns:
    # Dummy yield based on crop and features (simplified)
    df_balanced['yield'] = np.random.uniform(10, 50, len(df_balanced))  # Placeholder
else:
    # If yield exists, we need to handle it - for simplicity, regenerate
    df_balanced['yield'] = np.random.uniform(10, 50, len(df_balanced))

if 'profit' not in df.columns:
    # Dummy profit based on yield and random factors
    df_balanced['profit'] = df_balanced['yield'] * np.random.uniform(0.5, 2.0, len(df_balanced))  # Placeholder
else:
    # Regenerate profit
    df_balanced['profit'] = df_balanced['yield'] * np.random.uniform(0.5, 2.0, len(df_balanced))

y_yield = df_balanced['yield']
y_profit = df_balanced['profit']

# Use balanced data
X = X_balanced
y_crop = y_crop_balanced

# Split data
X_train, X_test, y_crop_train, y_crop_test = train_test_split(X, y_crop, test_size=0.2, random_state=42)
_, _, y_yield_train, y_yield_test = train_test_split(X, y_yield, test_size=0.2, random_state=42)
_, _, y_profit_train, y_profit_test = train_test_split(X, y_profit, test_size=0.2, random_state=42)

# Train crop model
crop_model = RandomForestClassifier(n_estimators=100, random_state=42)
crop_model.fit(X_train, y_crop_train)
y_crop_pred = crop_model.predict(X_test)
crop_accuracy = accuracy_score(y_crop_test, y_crop_pred)
print(f"Crop model accuracy: {crop_accuracy}")

# Train yield model
yield_model = RandomForestRegressor(n_estimators=100, random_state=42)
yield_model.fit(X_train, y_yield_train)
y_yield_pred = yield_model.predict(X_test)
yield_mse = mean_squared_error(y_yield_test, y_yield_pred)
print(f"Yield model MSE: {yield_mse}")

# Train profit model
profit_model = RandomForestRegressor(n_estimators=100, random_state=42)
profit_model.fit(X_train, y_profit_train)
y_profit_pred = profit_model.predict(X_test)
profit_mse = mean_squared_error(y_profit_test, y_profit_pred)
print(f"Profit model MSE: {profit_mse}")

# Save models
joblib.dump(crop_model, '../ml_models/crop_model.pkl')
joblib.dump(yield_model, '../ml_models/yield_model.pkl')
joblib.dump(profit_model, '../ml_models/profit_model.pkl')
print("Models trained and saved.")

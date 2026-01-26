import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('datasets/Crop_recommendation.csv')
df.fillna(df.mean(), inplace=True)
scaler = MinMaxScaler()
features = ['ph', 'humidity', 'N', 'P', 'K', 'temperature', 'rainfall']
df[features] = scaler.fit_transform(df[features])
df.to_csv('datasets/processed_crop_data.csv', index=False)
print("Tabular data processed.")

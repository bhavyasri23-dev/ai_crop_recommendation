import pandas as pd
import numpy as np

# Load existing dataset
df = pd.read_csv('../datasets/Crop_recommendation.csv')

# Define new crops and their typical parameter ranges
new_crops = {
    'wheat': {
        'N': (20, 40), 'P': (15, 30), 'K': (15, 30),
        'temperature': (10, 25), 'humidity': (40, 70),
        'ph': (6, 7.5), 'rainfall': (50, 100)
    },
    'cotton': {
        'N': (40, 80), 'P': (20, 40), 'K': (20, 40),
        'temperature': (20, 35), 'humidity': (50, 80),
        'ph': (6, 8), 'rainfall': (60, 120)
    },
    'sugarcane': {
        'N': (80, 120), 'P': (20, 40), 'K': (20, 40),
        'temperature': (20, 35), 'humidity': (70, 90),
        'ph': (6, 7.5), 'rainfall': (150, 250)
    },
    'soybean': {
        'N': (20, 40), 'P': (15, 30), 'K': (15, 30),
        'temperature': (20, 30), 'humidity': (60, 80),
        'ph': (6, 7), 'rainfall': (60, 100)
    },
    'barley': {
        'N': (20, 40), 'P': (15, 30), 'K': (15, 30),
        'temperature': (10, 25), 'humidity': (40, 70),
        'ph': (6, 7.5), 'rainfall': (40, 80)
    }
}

# Generate 100 samples for each new crop
new_data = []
for crop, ranges in new_crops.items():
    for _ in range(100):
        sample = {}
        for param, (min_val, max_val) in ranges.items():
            sample[param] = np.random.uniform(min_val, max_val)
        sample['label'] = crop
        new_data.append(sample)

# Create DataFrame for new data
new_df = pd.DataFrame(new_data)

# Append to existing dataset
expanded_df = pd.concat([df, new_df], ignore_index=True)

# Save expanded dataset
expanded_df.to_csv('../datasets/Crop_recommendation.csv', index=False)

print(f"Added {len(new_data)} samples for {len(new_crops)} new crops.")
print("Expanded dataset saved.")

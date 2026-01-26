# 🌾 Modular AI Agricultural Assistant

A production-ready, modular AI system providing **deterministic agricultural decision support** through two independent modules with strict single-output guarantees.

## 🏗️ Architecture

This system has been refactored from a monolithic application into **two strict and independent modules**:

### 🌾 Crop Recommendation Module (Port 5001)
- **Purpose**: Deterministic crop recommendations based on soil conditions
- **Input**: District + soil parameters (pH, N, P, rainfall)
- **Output**: **Exactly 1 crop** recommendation (no ambiguity, no multiple suggestions)
- **Technology**: Flask + Deterministic Rules Engine
- **Validation**: Cross-validates manual, satellite, and IoT sensor data

### 🔍 Disease Detection Module (Port 5002)
- **Purpose**: Single-output plant disease identification
- **Input**: Plant image + optional crop type
- **Output**: **Exactly 1 result** ("Healthy" or specific disease name)
- **Technology**: Flask + TensorFlow CNN
- **Validation**: Image quality assessment and leaf detection

### 🎨 Shared Frontend
- **Purpose**: Unified user interface routing requests to appropriate modules
- **Technology**: HTML/CSS/JavaScript
- **Features**: Automatic module detection and request routing

## ✨ Key Features

- ✅ **Strict Independence**: Zero shared code between modules
- ✅ **Deterministic Outputs**: Same inputs always produce same results
- ✅ **Single Clear Outputs**: No ambiguous recommendations
- ✅ **Input Validation**: Prevents mismatched data sources
- ✅ **Production Ready**: Clean, scalable, maintainable code
- ✅ **Cross-Platform**: Works on Windows, Linux, macOS

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Web browser

### Installation & Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd "croprecommendation app"
   ```

2. **Install dependencies for Crop Module**
   ```bash
   cd crop_recommendation_module
   pip install -r requirements.txt
   cd ..
   ```

3. **Install dependencies for Disease Module**
   ```bash
   cd disease_detection_module
   pip install -r requirements.txt
   cd ..
   ```

4. **Start the Crop Recommendation Module**
   ```bash
   cd crop_recommendation_module
   python app.py
   ```
   Module will start on http://localhost:5001

5. **Start the Disease Detection Module** (in a new terminal)
   ```bash
   cd disease_detection_module
   python app.py
   ```
   Module will start on http://localhost:5002

6. **Open the Shared Frontend**
   Open `shared_frontend/index.html` in your web browser

## 🧪 Testing

Run the comprehensive test suite to verify module functionality:

```bash
python test_refactored_modules.py
```

Tests include:
- ✅ Module independence verification
- ✅ Deterministic behavior validation
- ✅ Single-output constraints
- ✅ Input validation testing

## 📡 API Documentation

### Crop Recommendation Module (Port 5001)

#### POST `/api/recommend_crop`
Get deterministic crop recommendation.

**Request:**
```json
{
  "district": "Anantapur",
  "pH": 7.2,
  "nitrogen": 45,
  "phosphorus": 25,
  "rainfall": 550,
  "satellite_data": {
    "pH": 7.1,
    "nitrogen": 48,
    "phosphorus": 26,
    "rainfall": 560
  },
  "sensor_data": {
    "pH": 7.3,
    "nitrogen": 44,
    "phosphorus": 24,
    "rainfall": 555
  }
}
```

**Response:**
```json
{
  "data": {
    "recommendation": {
      "crop": "Groundnut",
      "confidence": 0.95,
      "reason": "Optimal conditions for groundnut in Anantapur region",
      "suitability_score": 8.5
    },
    "input_summary": {
      "district": "Anantapur",
      "region": "Rayalaseema",
      "soil_type": "Red Soil",
      "pH": 7.2,
      "nitrogen": 45,
      "phosphorus": 25,
      "rainfall": 550,
      "data_source": "manual"
    },
    "soil_fingerprint": "7.0_45_25_550",
    "validation_status": "passed"
  }
}
```

#### GET `/api/get_districts`
Get list of valid Andhra Pradesh districts.

#### POST `/api/validate_soil_data`
Validate consistency between different data sources.

### Disease Detection Module (Port 5002)

#### POST `/api/detect_disease`
Analyze plant image for disease detection.

**Request:**
```json
{
  "image": "base64_encoded_image_data",
  "crop_type": "rice"
}
```

**Response:**
```json
{
  "data": {
    "prediction": "Rice Bacterial Blight",
    "confidence": 0.87,
    "crop_type": "rice",
    "model_used": "CNN_Classifier",
    "processing_status": "success"
  }
}
```

#### GET `/api/get_supported_crops`
Get list of supported crop types for disease detection.

## 🎯 Design Principles

### Strict Module Independence
- No shared code, variables, or dependencies between modules
- Each module can be deployed, updated, and scaled independently
- Clear separation of concerns

### Deterministic Outputs
- **Crop Module**: Same soil conditions + district = same crop recommendation
- **Disease Module**: Same image = same disease prediction
- No randomness or probabilistic outputs

### Single Clear Outputs
- **Crop Module**: Returns exactly one crop (no "top 3" or multiple suggestions)
- **Disease Module**: Returns exactly one result ("Healthy" or specific disease)

### Input Validation
- Cross-validation between manual, satellite, and sensor data
- Prevents inconsistent or mismatched data sources
- Clear error messages for invalid inputs

## 🛠️ Development

### Project Structure
```
├── crop_recommendation_module/
│   ├── app.py                 # Flask application
│   ├── core/
│   │   ├── deterministic_mapper.py
│   │   ├── soil_validator.py
│   │   └── ap_districts.py
│   ├── data/
│   │   ├── crop_rules.json
│   │   └── district_data.json
│   └── requirements.txt
├── disease_detection_module/
│   ├── app.py                 # Flask application
│   ├── core/
│   │   ├── single_output_detector.py
│   │   ├── image_processor.py
│   │   └── model_manager.py
│   ├── models/                # Pretrained models
│   └── requirements.txt
├── shared_frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── test_refactored_modules.py  # Comprehensive test suite
└── README.md
```

### Adding New Crops/Diseases
- **Crop Module**: Update `crop_rules.json` with new deterministic mappings
- **Disease Module**: Add new disease classes to the CNN model and update class names

## 🤝 Contributing

1. Ensure all changes maintain module independence
2. Add tests for new functionality
3. Update documentation
4. Verify deterministic behavior is preserved

## 📄 License

This project is part of an AI agricultural assistant system designed for deterministic, reliable agricultural decision support.

## 🆘 Troubleshooting

### Modules Won't Start
- Ensure Python 3.8+ is installed
- Install requirements: `pip install -r requirements.txt`
- Check for port conflicts (5001/5002)

### Frontend Not Loading
- Ensure both backend modules are running
- Check browser console for CORS errors
- Verify file paths in shared_frontend

### Test Failures
- Run `python test_refactored_modules.py` for detailed diagnostics
- Check module logs for specific error messages
- Verify all dependencies are installed

---

**Built for reliability, precision, and agricultural decision support.** 🌱

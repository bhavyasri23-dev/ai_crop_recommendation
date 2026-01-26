
# Test data for different sections of the Crop Recommendation App

# 1. Crop Prediction Test Data (Web Form Inputs)
crop_prediction_test_data = [
    {
        "description": "Rice growing conditions",
        "web_inputs": {
            "ph": 6.5,
            "moisture": 82.0,
            "n": 90,
            "p": 42,
            "k": 43,
            "temp": 20.88,
            "rainfall": 202.94,
            "location": "Delhi, India"
        },
        "expected_output": "Rice"
    },
    {
        "description": "Wheat growing conditions",
        "web_inputs": {
            "ph": 6.8,
            "moisture": 60.0,
            "n": 40,
            "p": 50,
            "k": 20,
            "temp": 15.0,
            "rainfall": 150.0,
            "location": "Punjab, India"
        },
        "expected_output": "Wheat"
    },
    {
        "description": "Maize growing conditions",
        "web_inputs": {
            "ph": 6.0,
            "moisture": 70.0,
            "n": 80,
            "p": 40,
            "k": 40,
            "temp": 25.0,
            "rainfall": 180.0,
            "location": "Maharashtra, India"
        },
        "expected_output": "Maize"
    },
    {
        "description": "Cotton growing conditions",
        "web_inputs": {
            "ph": 7.5,
            "moisture": 50.0,
            "n": 120,
            "p": 40,
            "k": 20,
            "temp": 28.0,
            "rainfall": 80.0,
            "location": "Gujarat, India"
        },
        "expected_output": "Cotton"
    },
    {
        "description": "Sugarcane growing conditions",
        "web_inputs": {
            "ph": 6.8,
            "moisture": 75.0,
            "n": 150,
            "p": 80,
            "k": 50,
            "temp": 27.0,
            "rainfall": 180.0,
            "location": "Uttar Pradesh, India"
        },
        "expected_output": "Sugarcane"
    }
]

# 2. Disease Prediction Test Data (Web Form Inputs with Expected Results)
disease_prediction_test_data = [
    {
        "description": "Healthy Rice leaf",
        "web_inputs": {
            "image": "plant_disease_images/healthy_rice.jpg",
            "crop_type": "rice"
        },
        "expected_output": "Healthy"
    },
    {
        "description": "Rice leaf with blight",
        "web_inputs": {
            "image": "plant_disease_images/rice_blight.jpg",
            "crop_type": "rice"
        },
        "expected_output": "Leaf Blight"
    },
    {
        "description": "Wheat leaf with rust",
        "web_inputs": {
            "image": "plant_disease_images/wheat_rust.jpg",
            "crop_type": "wheat"
        },
        "expected_output": "Rust"
    },
    {
        "description": "Tomato leaf with blight",
        "web_inputs": {
            "image": "plant_disease_images/tomato_blight.jpg",
            "crop_type": "tomato"
        },
        "expected_output": "Leaf Blight"
    },
    {
        "description": "Potato leaf with late blight",
        "web_inputs": {
            "image": "plant_disease_images/potato_blight.jpg",
            "crop_type": "potato"
        },
        "expected_output": "Late Blight"
    }
]

# 3. Weather Integration Test Data (Web Form Inputs with Expected Results)
weather_test_data = [
    {
        "description": "Delhi weather forecast",
        "web_inputs": {
            "weather-location": "Delhi, India"
        },
        "expected_output": {
            "temperature": "15-35°C",
            "humidity": "30-70%",
            "rainfall": "Low to moderate",
            "conditions": "Clear to partly cloudy"
        }
    },
    {
        "description": "Mumbai weather forecast",
        "web_inputs": {
            "weather-location": "Mumbai, India"
        },
        "expected_output": {
            "temperature": "25-35°C",
            "humidity": "60-90%",
            "rainfall": "Moderate to high",
            "conditions": "Humid with possible showers"
        }
    },
    {
        "description": "Bangalore weather forecast",
        "web_inputs": {
            "weather-location": "Bangalore, India"
        },
        "expected_output": {
            "temperature": "20-30°C",
            "humidity": "50-80%",
            "rainfall": "Low to moderate",
            "conditions": "Pleasant with occasional rain"
        }
    },
    {
        "description": "Chennai weather forecast",
        "web_inputs": {
            "weather-location": "Chennai, India"
        },
        "expected_output": {
            "temperature": "25-35°C",
            "humidity": "70-90%",
            "rainfall": "Moderate",
            "conditions": "Hot and humid"
        }
    }
]

# 4. Translation Test Data
translation_test_data = [
    {
        "description": "English translations",
        "lang": "en"
    },
    {
        "description": "Hindi translations",
        "lang": "hi"
    },
    {
        "description": "Spanish translations",
        "lang": "es"
    }
]

# 5. Satellite Soil Data Test Data
satellite_soil_test_data = [
    {
        "description": "Delhi soil data",
        "lat": 28.6139,
        "lon": 77.2090
    },
    {
        "description": "Mumbai soil data",
        "lat": 19.0760,
        "lon": 72.8777
    },
    {
        "description": "Bangalore soil data",
        "lat": 12.9716,
        "lon": 77.5946
    }
]

# 6. Satellite Weather Data Test Data
satellite_weather_test_data = [
    {
        "description": "Delhi satellite weather",
        "lat": 28.6139,
        "lon": 77.2090
    },
    {
        "description": "Mumbai satellite weather",
        "lat": 19.0760,
        "lon": 72.8777
    }
]

# 7. IoT Sensor Test Data
iot_sensor_test_data = [
    {
        "description": "Connect soil sensor",
        "endpoint": "/api/iot/connect_sensor",
        "method": "POST",
        "data": {
            "sensor_id": "SOIL_001",
            "sensor_type": "soil_sensor",
            "protocol": "mqtt"
        }
    },
    {
        "description": "Connect temperature sensor",
        "endpoint": "/api/iot/connect_sensor",
        "method": "POST",
        "data": {
            "sensor_id": "TEMP_001",
            "sensor_type": "temperature_sensor",
            "protocol": "mqtt"
        }
    },
    {
        "description": "Disconnect sensor",
        "endpoint": "/api/iot/disconnect_sensor",
        "method": "POST",
        "data": {
            "sensor_id": "SOIL_001"
        }
    },
    {
        "description": "Get sensor data",
        "endpoint": "/api/iot/sensor_data/SOIL_001",
        "method": "GET",
        "params": {
            "hours": 24
        }
    },
    {
        "description": "Get connected sensors",
        "endpoint": "/api/iot/connected_sensors",
        "method": "GET"
    },
    {
        "description": "Get sensor status",
        "endpoint": "/api/iot/sensor_status/SOIL_001",
        "method": "GET"
    }
]

# 8. Export Test Data
export_test_data = [
    {
        "description": "Crop recommendation PDF export",
        "endpoint": "/api/export_crop_pdf",
        "method": "POST",
        "data": {
            "data": {
                "N": 90,
                "P": 42,
                "K": 43,
                "temperature": 20.879744,
                "humidity": 82.002744,
                "ph": 6.502985,
                "rainfall": 202.935536
            },
            "result": {
                "predicted_crop": "Rice"
            }
        }
    },
    {
        "description": "Disease detection PDF export",
        "endpoint": "/api/export_disease_pdf",
        "method": "POST",
        "data": {
            "data": {
                "crop_type": "Rice",
                "image_info": "Leaf image analysis"
            },
            "result": {
                "predicted_disease": "Leaf Blight"
            }
        }
    }
]

# 9. Market Commodity Test Data (Web Form Inputs with Expected Results)
market_commodity_test_data = [
    {
        "description": "Rice market prices",
        "web_inputs": {
            "commodity": "rice",
            "market-location": "Delhi, India"
        },
        "expected_output": {
            "current_price": "₹25-35/kg",
            "trend": "Stable to increasing",
            "demand": "High"
        }
    },
    {
        "description": "Wheat market prices",
        "web_inputs": {
            "commodity": "wheat",
            "market-location": "Punjab, India"
        },
        "expected_output": {
            "current_price": "₹20-30/kg",
            "trend": "Stable",
            "demand": "Medium"
        }
    },
    {
        "description": "Cotton market prices",
        "web_inputs": {
            "commodity": "cotton",
            "market-location": "Gujarat, India"
        },
        "expected_output": {
            "current_price": "₹50-70/kg",
            "trend": "Increasing",
            "demand": "High"
        }
    },
    {
        "description": "Sugarcane market prices",
        "web_inputs": {
            "commodity": "sugarcane",
            "market-location": "Uttar Pradesh, India"
        },
        "expected_output": {
            "current_price": "₹300-400/ton",
            "trend": "Stable",
            "demand": "Medium"
        }
    }
]

# 10. Disease Detection Crop Types Test Data (for web app dropdowns)
disease_detection_crop_types = [
    "Rice", "Wheat", "Maize", "Cotton", "Sugarcane",
    "Soybean", "Barley", "Potato", "Tomato", "Onion",
    "Groundnut", "Mustard", "Sunflower"
]

if __name__ == "__main__":
    print("Test data loaded successfully!")
    print(f"Crop prediction test cases: {len(crop_prediction_test_data)}")
    print(f"Weather test cases: {len(weather_test_data)}")
    print(f"IoT sensor test cases: {len(iot_sensor_test_data)}")
    print(f"Market commodities: {len(market_commodity_test_data)}")

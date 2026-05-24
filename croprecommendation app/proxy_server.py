#!/usr/bin/env python3
"""
Proxy server to run both modules on localhost:5000
Routes requests based on endpoints:
- /api/recommend_crop, /api/get_districts, /api/validate_soil_data, /api/get_crop_characteristics → Crop Module (port 5001)
- /api/predict_disease → Disease Module (port 5002)
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import threading
import subprocess
import sys
import os
import time

app = Flask(__name__)
CORS(app)

# Module URLs
# Crop module runs on 5002, disease module runs on 5003
CROP_MODULE_URL = "http://localhost:5002"
DISEASE_MODULE_URL = "http://localhost:5003"

def start_crop_module():
    """Start crop recommendation module on port 5002"""
    print("🌾 Starting Crop Recommendation Module on port 5002...")
    crop_dir = os.path.join(os.path.dirname(__file__), 'crop_recommendation_module')
    subprocess.run([sys.executable, 'app.py'], cwd=crop_dir)

def start_disease_module():
    """Start disease detection module on port 5003"""
    print("🔬 Starting Disease Detection Module on port 5003...")
    time.sleep(2)  # Delay to let crop module start first
    disease_dir = os.path.join(os.path.dirname(__file__), 'disease_detection_module')
    subprocess.run([sys.executable, 'app.py'], cwd=disease_dir)

@app.route('/api/recommend_crop', methods=['POST'])
def proxy_crop_recommendation():
    """Proxy crop recommendation requests"""
    try:
        response = requests.post(f"{CROP_MODULE_URL}/api/recommend_crop", json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Crop module unavailable: {str(e)}'}), 503

@app.route('/api/validate_soil_data', methods=['POST'])
def proxy_validate_soil():
    """Proxy soil data validation requests"""
    try:
        response = requests.post(f"{CROP_MODULE_URL}/api/validate_soil_data", json=request.get_json())
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Crop module unavailable: {str(e)}'}), 503

@app.route('/api/get_districts', methods=['GET'])
def proxy_get_districts():
    """Proxy get districts requests"""
    try:
        response = requests.get(f"{CROP_MODULE_URL}/api/get_districts")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Crop module unavailable: {str(e)}'}), 503

@app.route('/api/get_crop_characteristics', methods=['GET'])
def proxy_get_crop_characteristics():
    """Proxy get crop characteristics requests"""
    try:
        response = requests.get(f"{CROP_MODULE_URL}/api/get_crop_characteristics", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Crop module unavailable: {str(e)}'}), 503

@app.route('/api/predict_disease', methods=['POST'])
@app.route('/api/detect_disease', methods=['POST'])
def proxy_disease_prediction():
    """Proxy disease prediction requests"""
    try:
        # Forward the multipart form data
        files = {}
        data = {}

        if 'image' in request.files:
            files['image'] = request.files['image']
        
        if 'crop_type' in request.form:
            data['crop_type'] = request.form['crop_type']

        # Forward to the supported disease endpoint
        response = requests.post(
            f"{DISEASE_MODULE_URL}/api/detect_disease",
            files=files,
            data=data,
            timeout=30
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Disease module unavailable: {str(e)}'}), 503

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve the shared frontend"""
    try:
        return send_from_directory('shared_frontend', path)
    except FileNotFoundError:
        if not path.startswith('api/'):
            return send_from_directory('shared_frontend', 'index.html')
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/get_weather', methods=['GET'])
def proxy_get_weather():
    """Proxy weather requests - simulated for now"""
    location = request.args.get('location', 'Anantapur')
    # Simulate weather data
    import random
    weather_data = {
        'temperature': round(random.uniform(20, 35), 1),
        'humidity': round(random.uniform(40, 80), 1),
        'description': random.choice(['Sunny', 'Cloudy', 'Partly cloudy', 'Clear sky']),
        'location': location
    }
    return jsonify(weather_data)

@app.route('/api/export_crop_pdf', methods=['POST'])
def proxy_export_crop_pdf():
    """Proxy crop PDF export - simulated for now"""
    # In a real implementation, this would generate a PDF
    return jsonify({'error': 'PDF export not implemented yet'}), 501

@app.route('/api/export_disease_pdf', methods=['POST'])
def proxy_export_disease_pdf():
    """Proxy disease PDF export - simulated for now"""
    # In a real implementation, this would generate a PDF
    return jsonify({'error': 'PDF export not implemented yet'}), 501

@app.route('/api/satellite/soil_data', methods=['GET'])
def proxy_satellite_soil_data():
    """Proxy satellite soil data - simulated for now"""
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude required'}), 400

    # Simulate satellite soil data
    import random
    soil_data = {
        'ph': round(random.uniform(5.5, 8.5), 2),
        'nitrogen': round(random.uniform(20, 100), 1),
        'phosphorus': round(random.uniform(15, 60), 1),
        'potassium': round(random.uniform(100, 300), 1),
        'data_source': 'Simulated Satellite Data',
        'confidence': '85%'
    }
    return jsonify(soil_data)

@app.route('/api/iot/connect_sensor', methods=['POST'])
def proxy_connect_iot_sensor():
    """Proxy IoT sensor connection - simulated for now"""
    data = request.get_json()
    sensor_id = data.get('sensor_id', 'unknown')
    return jsonify({
        'sensor_id': sensor_id,
        'protocol': 'mqtt',
        'connected_at': '2024-01-01T00:00:00Z',
        'status': 'connected'
    })

@app.route('/api/iot/sensor_data/<sensor_id>', methods=['GET', 'POST'])
def proxy_iot_sensor_data(sensor_id):
    """Proxy IoT sensor data - simulated for now"""
    import random
    from datetime import datetime

    # Check if manual values were provided
    if request.method == 'POST':
        manual_data = request.get_json().get('manual_values', {})
        sensor_data = {
            'sensor_id': sensor_id,
            'latest_reading': {
                'moisture': float(manual_data.get('moisture', random.uniform(30, 70))),
                'temperature': float(manual_data.get('temp', random.uniform(20, 35))),
                'ph': float(manual_data.get('ph', random.uniform(5.5, 8.5))),
                'rainfall': float(manual_data.get('rainfall', random.uniform(50, 150))),
                'nitrogen': float(manual_data.get('n', random.uniform(20, 100))),
                'phosphorus': float(manual_data.get('p', random.uniform(15, 60))),
                'potassium': float(manual_data.get('k', random.uniform(100, 300))),
                'timestamp': datetime.now().isoformat()
            }
        }
    else:
        sensor_data = {
            'sensor_id': sensor_id,
            'latest_reading': {
                'moisture': round(random.uniform(30, 70), 2),
                'temperature': round(random.uniform(20, 35), 2),
                'ph': round(random.uniform(5.5, 8.5), 2),
                'rainfall': round(random.uniform(50, 150), 2),
                'nitrogen': round(random.uniform(20, 100), 1),
                'phosphorus': round(random.uniform(15, 60), 1),
                'potassium': round(random.uniform(100, 300), 1),
                'timestamp': datetime.now().isoformat()
            }
        }
    return jsonify(sensor_data)

@app.route('/api/iot/connected_sensors', methods=['GET'])
def proxy_connected_sensors():
    """Proxy connected IoT sensors - simulated for now"""
    sensors = [
        {'sensor_id': 'AP001', 'location': 'Anantapur'},
        {'sensor_id': 'AP002', 'location': 'Chittoor'},
        {'sensor_id': 'AP003', 'location': 'East Godavari'},
        {'sensor_id': 'AP004', 'location': 'Guntur'}
    ]
    return jsonify(sensors)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'modules': {
            'crop_recommendation': f"{CROP_MODULE_URL}/health",
            'disease_detection': f"{DISEASE_MODULE_URL}/health"
        }
    })

if __name__ == '__main__':
    print("🚀 Starting AI Crop Recommendation System Proxy")
    print("===============================================")
    print("🌐 Proxy Server: http://localhost:5000")
    print("🌾 Crop Module: http://localhost:5002")
    print("🔬 Disease Module: http://localhost:5003")
    print("Press Ctrl+C to stop all modules")
    print("===============================================")

    # Start both modules in background threads
    crop_thread = threading.Thread(target=start_crop_module, daemon=True)
    disease_thread = threading.Thread(target=start_disease_module, daemon=True)

    crop_thread.start()
    disease_thread.start()

    # Give modules time to start
    time.sleep(3)

    try:
        # Start proxy server on port 5000
        print("🌐 Starting Proxy Server on port 5000...")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all modules...")
        sys.exit(0)

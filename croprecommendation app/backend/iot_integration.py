
"""
IoT integration module for sensor data management
"""

def connect_iot_sensor(sensor_id, sensor_type, protocol):
    """
    Connect to an IoT sensor
    """
    # Mock implementation
    return {
        'status': 'connected',
        'sensor_id': sensor_id,
        'sensor_type': sensor_type,
        'protocol': protocol
    }

def disconnect_iot_sensor(sensor_id):
    """
    Disconnect from an IoT sensor
    """
    # Mock implementation
    return {
        'status': 'disconnected',
        'sensor_id': sensor_id
    }

def get_iot_sensor_data(sensor_id, hours=24, manual_values=None):
    """
    Get sensor data for specified hours
    If manual_values are provided, use them instead of sensor data for prediction
    """
    # Mock implementation
    import random
    import datetime

    # Check if manual values are provided and use them
    if manual_values:
        print(f"Using manual values for sensor {sensor_id}: {manual_values}")
        # Use manual values directly for the latest reading
        latest_reading = {
            'temperature': float(manual_values.get('temp', 25.0)),
            'moisture': float(manual_values.get('moisture', 45.0)),
            'ph': float(manual_values.get('ph', 6.5)),
            'nitrogen': float(manual_values.get('n', 50)),
            'phosphorus': float(manual_values.get('p', 30)),
            'potassium': float(manual_values.get('k', 200)),
            'rainfall': float(manual_values.get('rainfall', 100.0)),
            'timestamp': datetime.datetime.now().isoformat()
        }

        # Create historical data arrays with slight variations around manual values
        base_temp = float(manual_values.get('temp', 25.0))
        base_moisture = float(manual_values.get('moisture', 45.0))
        base_ph = float(manual_values.get('ph', 6.5))
        base_n = float(manual_values.get('n', 50))
        base_p = float(manual_values.get('p', 30))
        base_k = float(manual_values.get('k', 200))
        base_rainfall = float(manual_values.get('rainfall', 100.0))

        historical_data = {
            'sensor_id': sensor_id,
            'data_points': hours,
            'latest_reading': latest_reading,
            'temperature': [round(base_temp + random.uniform(-1, 1), 2) for i in range(hours)],
            'humidity': [round(65.0 + random.uniform(-5, 5), 2) for i in range(hours)],
            'soil_moisture': [round(base_moisture + random.uniform(-2, 2), 2) for i in range(hours)],
            'ph': [round(base_ph + random.uniform(-0.2, 0.2), 2) for i in range(hours)],
            'nitrogen': [round(base_n + random.uniform(-5, 5), 2) for i in range(hours)],
            'phosphorus': [round(base_p + random.uniform(-3, 3), 2) for i in range(hours)],
            'potassium': [round(base_k + random.uniform(-10, 10), 2) for i in range(hours)],
            'timestamps': [(datetime.datetime.now() - datetime.timedelta(hours=i)).isoformat() for i in range(hours)]
        }

        return historical_data

    # District-specific soil conditions for Andhra Pradesh to ensure appropriate crop recommendations
    sensor_configs = {
        'ASU-AP-01-Ananthpur': {
            'temp': 28.0,  # Groundnut/cotton region: 25-35°C
            'moisture': 35.0,  # Arid region: 30-50%
            'ph': 6.2,  # Red sandy soils: 5.5-7.0
            'rainfall': 60.0,  # Semi-arid: 50-70cm
            'n': 45,  # Moderate nitrogen for groundnuts
            'p': 35,
            'k': 150
        },
        'ASU-AP-02-Chittoor': {
            'temp': 26.0,  # Fruit/vegetable region: 20-30°C
            'moisture': 50.0,  # Moderate moisture: 40-60%
            'ph': 6.5,  # Red loamy soils: 6.0-7.5
            'rainfall': 90.0,  # Moderate rainfall: 80-100cm
            'n': 55,  # Higher nitrogen for fruits/vegetables
            'p': 40,
            'k': 200
        },
        'ASU-AP-03-EastGodavari': {
            'temp': 27.0,  # Rice/coconut region: 25-30°C
            'moisture': 65.0,  # High moisture for rice: 60-80%
            'ph': 6.8,  # Alluvial soils: 6.5-7.5
            'rainfall': 120.0,  # High rainfall delta: 110-130cm
            'n': 60,  # High nitrogen for rice
            'p': 45,
            'k': 180
        },
        'ASU-AP-04-Guntur': {
            'temp': 15.0,  # Barley optimal: 10-25°C (adjusted lower for barley)
            'moisture': 45.0,  # Barley optimal: 40-70% (adjusted lower for barley)
            'ph': 6.8,  # Barley optimal: 6.0-8.0
            'rainfall': 50.0,  # Barley optimal: 40-80mm (adjusted lower for barley)
            'n': 35,  # Lower nitrogen for barley
            'p': 25,
            'k': 180
        },
        'ASU-AP-05-Krishna': {
            'temp': 27.0,  # Rice/tobacco region: 25-30°C
            'moisture': 60.0,  # Moderate-high moisture: 50-70%
            'ph': 7.0,  # Mixed alluvial/black soils: 6.5-7.5
            'rainfall': 95.0,  # Moderate rainfall: 90-100cm
            'n': 50,  # Moderate nitrogen
            'p': 35,
            'k': 190
        },
        'ASU-AP-06-Kurnool': {
            'temp': 29.0,  # Groundnut/sunflower region: 25-35°C
            'moisture': 40.0,  # Semi-arid: 35-50%
            'ph': 6.0,  # Red sandy soils: 5.5-6.5
            'rainfall': 65.0,  # Low-moderate rainfall: 60-70cm
            'n': 40,  # Moderate nitrogen for dry crops
            'p': 30,
            'k': 140
        },
        'ASU-AP-07-Prakasam': {
            'temp': 32.0,  # Cotton/tobacco region: 28-35°C (well above barley optimal of 10-25°C)
            'moisture': 48.0,  # Moderate moisture: 40-55%
            'ph': 7.5,  # Black cotton soils: 7.0-8.0 (higher than barley optimal)
            'rainfall': 85.0,  # Moderate rainfall: 70-80cm (higher than barley optimal)
            'n': 60,  # Higher nitrogen for cotton/tobacco
            'p': 45,
            'k': 250  # Higher potassium for cotton
        },
        'ASU-AP-08-Srikakulam': {
            'temp': 26.0,  # Rice/coconut region: 24-28°C
            'moisture': 70.0,  # High moisture coastal: 65-80%
            'ph': 6.5,  # Coastal alluvial: 6.0-7.0
            'rainfall': 110.0,  # High coastal rainfall: 100-120cm
            'n': 65,  # High nitrogen for rice
            'p': 50,
            'k': 170
        },
        'ASU-AP-09-Nellore': {
            'temp': 28.0,  # Rice/groundnut region: 25-32°C
            'moisture': 55.0,  # Moderate moisture: 50-65%
            'ph': 6.8,  # Mixed coastal soils: 6.5-7.5
            'rainfall': 105.0,  # Moderate-high rainfall: 100-110cm
            'n': 50,  # Moderate nitrogen
            'p': 35,
            'k': 160
        },
        'ASU-AP-10-Visakhapatnam': {
            'temp': 27.0,  # Rice/coconut region: 25-30°C
            'moisture': 68.0,  # High coastal moisture: 60-75%
            'ph': 6.3,  # Coastal lateritic: 5.5-7.0
            'rainfall': 115.0,  # High coastal rainfall: 110-120cm
            'n': 58,  # Moderate-high nitrogen
            'p': 42,
            'k': 175
        },
        'ASU-AP-11-Vijayawada': {
            'temp': 27.5,  # Rice/tobacco region: 25-30°C
            'moisture': 62.0,  # Moderate-high moisture: 55-70%
            'ph': 7.1,  # Delta soils: 6.8-7.5
            'rainfall': 98.0,  # Moderate-high rainfall: 95-105cm
            'n': 52,  # Moderate nitrogen
            'p': 38,
            'k': 185
        },
        'ASU-AP-12-WestGodavari': {
            'temp': 27.0,  # Rice/sugarcane region: 25-30°C
            'moisture': 66.0,  # High moisture delta: 60-75%
            'ph': 6.9,  # Alluvial delta soils: 6.5-7.5
            'rainfall': 118.0,  # High delta rainfall: 115-125cm
            'n': 62,  # High nitrogen for sugarcane
            'p': 48,
            'k': 195
        },
        'ASU-AP-13-Kadapa': {
            'temp': 28.5,  # Groundnut/cotton region: 25-32°C
            'moisture': 42.0,  # Semi-arid: 35-50%
            'ph': 6.4,  # Red sandy soils: 6.0-7.0
            'rainfall': 70.0,  # Moderate rainfall: 65-75cm
            'n': 42,  # Moderate nitrogen
            'p': 32,
            'k': 155
        }
    }

    # Get sensor-specific config or use defaults
    config = sensor_configs.get(sensor_id, {
        'temp': 25.0,
        'moisture': 45.0,
        'ph': 6.5,
        'rainfall': 100.0,
        'n': 50,
        'p': 30,
        'k': 200
    })

    # Generate mock sensor readings with sensor-specific base values
    # Reduce random variation for Guntur sensor to ensure consistent barley prediction
    # Reduce variation for Prakasam to ensure consistent cotton/tobacco prediction
    if sensor_id == 'ASU-AP-04-Guntur':
        base_temp = config['temp'] + random.uniform(-1, 1)  # Reduced variation
        base_moisture = config['moisture'] + random.uniform(-3, 3)  # Reduced variation
        base_ph = config['ph'] + random.uniform(-0.2, 0.2)  # Reduced variation
        base_n = config['n'] + random.uniform(-5, 5)  # Reduced variation
        base_p = config['p'] + random.uniform(-3, 3)  # Reduced variation
        base_k = config['k'] + random.uniform(-10, 10)  # Reduced variation
        base_rainfall = config['rainfall'] + random.uniform(-5, 5)  # Reduced variation
    elif sensor_id == 'ASU-AP-07-Prakasam':
        base_temp = config['temp'] + random.uniform(-1, 1)  # Reduced variation for cotton/tobacco
        base_moisture = config['moisture'] + random.uniform(-3, 3)  # Reduced variation
        base_ph = config['ph'] + random.uniform(-0.2, 0.2)  # Reduced variation
        base_n = config['n'] + random.uniform(-5, 5)  # Reduced variation
        base_p = config['p'] + random.uniform(-3, 3)  # Reduced variation
        base_k = config['k'] + random.uniform(-10, 10)  # Reduced variation
        base_rainfall = config['rainfall'] + random.uniform(-5, 5)  # Reduced variation
    else:
        base_temp = config['temp'] + random.uniform(-3, 3)
        base_moisture = config['moisture'] + random.uniform(-8, 8)
        base_ph = config['ph'] + random.uniform(-0.5, 0.5)
        base_n = config['n'] + random.uniform(-10, 10)
        base_p = config['p'] + random.uniform(-8, 8)
        base_k = config['k'] + random.uniform(-30, 30)
        base_rainfall = config['rainfall'] + random.uniform(-20, 20)

    # Create latest reading object
    latest_reading = {
        'temperature': round(base_temp, 2),
        'moisture': round(base_moisture, 2),
        'ph': round(base_ph, 2),
        'nitrogen': round(base_n, 2),
        'phosphorus': round(base_p, 2),
        'potassium': round(base_k, 2),
        'rainfall': round(base_rainfall, 2),
        'timestamp': datetime.datetime.now().isoformat()
    }

    # Create historical data arrays
    historical_data = {
        'sensor_id': sensor_id,
        'data_points': hours,
        'latest_reading': latest_reading,
        'temperature': [round(base_temp + i*0.1 + random.uniform(-1, 1), 2) for i in range(hours)],
        'humidity': [round(65.0 + i*0.2 + random.uniform(-5, 5), 2) for i in range(hours)],
        'soil_moisture': [round(base_moisture + i*0.1 + random.uniform(-2, 2), 2) for i in range(hours)],
        'ph': [round(base_ph + random.uniform(-0.2, 0.2), 2) for i in range(hours)],
        'nitrogen': [round(base_n + random.uniform(-5, 5), 2) for i in range(hours)],
        'phosphorus': [round(base_p + random.uniform(-3, 3), 2) for i in range(hours)],
        'potassium': [round(base_k + random.uniform(-10, 10), 2) for i in range(hours)],
        'timestamps': [(datetime.datetime.now() - datetime.timedelta(hours=i)).isoformat() for i in range(hours)]
    }

    return historical_data

def get_connected_iot_sensors():
    """
    Get list of connected IoT sensors for Andhra Pradesh districts
    """
    # Mock implementation with sensors for Andhra Pradesh districts
    andhra_pradesh_sensors = [
        {
            'sensor_id': 'ASU-AP-01-Ananthpur',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Ananthpur District, Andhra Pradesh',
            'coordinates': {'lat': 14.68, 'lon': 77.60}
        },
        {
            'sensor_id': 'ASU-AP-02-Chittoor',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Chittoor District, Andhra Pradesh',
            'coordinates': {'lat': 13.22, 'lon': 79.10}
        },
        {
            'sensor_id': 'ASU-AP-03-EastGodavari',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'East Godavari District, Andhra Pradesh',
            'coordinates': {'lat': 17.24, 'lon': 81.89}
        },
        {
            'sensor_id': 'ASU-AP-04-Guntur',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Guntur District, Andhra Pradesh',
            'coordinates': {'lat': 16.31, 'lon': 80.44}
        },
        {
            'sensor_id': 'ASU-AP-05-Krishna',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Krishna District, Andhra Pradesh',
            'coordinates': {'lat': 16.51, 'lon': 80.92}
        },
        {
            'sensor_id': 'ASU-AP-06-Kurnool',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Kurnool District, Andhra Pradesh',
            'coordinates': {'lat': 15.83, 'lon': 78.04}
        },
        {
            'sensor_id': 'ASU-AP-07-Prakasam',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Prakasam District, Andhra Pradesh',
            'coordinates': {'lat': 15.51, 'lon': 79.99}
        },
        {
            'sensor_id': 'ASU-AP-08-Srikakulam',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Srikakulam District, Andhra Pradesh',
            'coordinates': {'lat': 18.30, 'lon': 83.90}
        },
        {
            'sensor_id': 'ASU-AP-09-Nellore',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Nellore District, Andhra Pradesh',
            'coordinates': {'lat': 14.44, 'lon': 79.99}
        },
        {
            'sensor_id': 'ASU-AP-10-Visakhapatnam',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Visakhapatnam District, Andhra Pradesh',
            'coordinates': {'lat': 17.69, 'lon': 83.21}
        },
        {
            'sensor_id': 'ASU-AP-11-Vijayawada',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Vijayawada, Krishna District, Andhra Pradesh',
            'coordinates': {'lat': 16.51, 'lon': 80.64}
        },
        {
            'sensor_id': 'ASU-AP-12-WestGodavari',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'West Godavari District, Andhra Pradesh',
            'coordinates': {'lat': 16.91, 'lon': 81.15}
        },
        {
            'sensor_id': 'ASU-AP-13-Kadapa',
            'sensor_type': 'soil_sensor',
            'status': 'connected',
            'location': 'Kadapa District, Andhra Pradesh',
            'coordinates': {'lat': 14.47, 'lon': 78.82}
        }
    ]

    return andhra_pradesh_sensors

def get_iot_sensor_status(sensor_id):
    """
    Get status of a specific IoT sensor
    """
    # Mock implementation
    return {
        'sensor_id': sensor_id,
        'status': 'connected',
        'last_seen': '2024-01-01T12:00:00Z',
        'battery_level': 85.0
    }

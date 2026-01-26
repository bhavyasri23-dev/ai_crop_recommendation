"""
Satellite integration module for soil and weather data
"""

def get_satellite_soil_data(latitude, longitude, manual_values=None):
    """
    Get satellite soil data
    If manual_values are provided, use them instead of satellite data for consistency
    """
    # Check if manual values are provided and use them
    if manual_values:
        print(f"Using manual soil values for satellite data: {manual_values}")
        return {
            'nitrogen': float(manual_values.get('n', 50.0)),
            'phosphorus': float(manual_values.get('p', 30.0)),
            'potassium': float(manual_values.get('k', 200.0)),
            'ph': float(manual_values.get('ph', 6.5)),
            'soil_type': manual_values.get('soil_type', 'Loam'),
            'latitude': latitude,
            'longitude': longitude
        }

    # Mock implementation with location-specific data for consistency
    # Guntur district coordinates (approx): 16.31, 80.44
    if 16.0 <= latitude <= 17.0 and 80.0 <= longitude <= 81.0:  # Guntur district
        return {
            'nitrogen': 35.0,  # Lower nitrogen for barley
            'phosphorus': 25.0,
            'potassium': 180.0,
            'ph': 6.8,  # Barley optimal pH
            'soil_type': 'Loam',
            'latitude': latitude,
            'longitude': longitude
        }
    else:
        # Default values for other locations
        return {
            'nitrogen': 45.0,
            'phosphorus': 35.0,
            'potassium': 45.0,
            'ph': 6.5,
            'soil_type': 'Loam',
            'latitude': latitude,
            'longitude': longitude
        }

def get_satellite_weather_data(latitude, longitude, manual_values=None):
    """
    Get satellite weather data
    If manual_values are provided, use them instead of satellite data for consistency
    """
    # Check if manual values are provided and use them
    if manual_values:
        print(f"Using manual weather values for satellite data: {manual_values}")
        return {
            'temperature': float(manual_values.get('temperature', 28.0)),
            'humidity': float(manual_values.get('humidity', 70.0)),
            'rainfall': float(manual_values.get('rainfall', 45.0)),
            'wind_speed': float(manual_values.get('wind_speed', 5.0)),
            'latitude': latitude,
            'longitude': longitude
        }

    # Mock implementation
    return {
        'temperature': 28.0,
        'humidity': 70.0,
        'rainfall': 45.0,
        'wind_speed': 5.0,
        'latitude': latitude,
        'longitude': longitude
    }

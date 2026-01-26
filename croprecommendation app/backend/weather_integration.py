"""
Weather integration module for crop recommendation system
"""

def get_weather_data(location, manual_values=None):
    """
    Get weather data for a location
    If manual_values are provided, use them instead of weather data for consistency
    """
    # Check if manual values are provided and use them
    if manual_values:
        print(f"Using manual weather values: {manual_values}")
        return {
            'temperature': float(manual_values.get('temperature', 25.0)),
            'humidity': float(manual_values.get('humidity', 65.0)),
            'rainfall': float(manual_values.get('rainfall', 50.0)),
            'location': location,
            'description': 'Manual values provided'
        }

    # Mock implementation
    return {
        'temperature': 25.0,
        'humidity': 65.0,
        'rainfall': 50.0,
        'location': location,
        'description': 'Partly cloudy'
    }

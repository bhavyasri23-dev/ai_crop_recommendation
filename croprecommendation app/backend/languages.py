"""
Language support module for internationalization
"""

def get_all_messages(language):
    """
    Get all messages for a language
    """
    # Mock implementation with basic messages
    messages = {
        'en': {
            'welcome': 'Welcome to Crop Recommendation System',
            'predict_crop': 'Predict Crop',
            'predict_disease': 'Predict Disease',
            'weather': 'Weather Information',
            'export': 'Export Results'
        },
        'es': {
            'welcome': 'Bienvenido al Sistema de Recomendación de Cultivos',
            'predict_crop': 'Predecir Cultivo',
            'predict_disease': 'Predecir Enfermedad',
            'weather': 'Información del Clima',
            'export': 'Exportar Resultados'
        },
        'hi': {
            'welcome': 'फसल अनुशंसा प्रणाली में आपका स्वागत है',
            'predict_crop': 'फसल की भविष्यवाणी करें',
            'predict_disease': 'बीमारी की भविष्यवाणी करें',
            'weather': 'मौसम की जानकारी',
            'export': 'परिणाम निर्यात करें'
        }
    }
    return messages.get(language, messages['en'])

def get_supported_languages():
    """
    Get list of supported languages
    """
    return [
        {'code': 'en', 'name': 'English'},
        {'code': 'es', 'name': 'Español'},
        {'code': 'hi', 'name': 'हिंदी'}
    ]

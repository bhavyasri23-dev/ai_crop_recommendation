"""
Recommender Module for Grove AI

Provides treatment recommendations, causes, and prevention tips for detected plant diseases.
"""

import logging

logger = logging.getLogger(__name__)

class DiseaseRecommender:
    """
    Provides recommendations for plant disease treatment and prevention.
    """

    # Comprehensive disease database with recommendations
    DISEASE_DATABASE = {
        # Tomato diseases
        'tomato': {
            'healthy': {
                'cause': 'No disease detected',
                'treatment': 'Continue regular care and monitoring',
                'prevention': 'Maintain proper watering, fertilization, and pest monitoring'
            },
            'bacterial_spot': {
                'cause': 'Caused by Xanthomonas bacteria, spread through water and infected seeds',
                'treatment': 'Remove infected leaves, apply copper-based fungicides, avoid overhead watering',
                'prevention': 'Use disease-resistant varieties, rotate crops, avoid working with wet plants'
            },
            'early_blight': {
                'cause': 'Fungal disease caused by Alternaria solani, thrives in warm, humid conditions',
                'treatment': 'Remove affected leaves, apply fungicides containing chlorothalonil or copper',
                'prevention': 'Improve air circulation, water at soil level, mulch around plants'
            },
            'late_blight': {
                'cause': 'Oomycete pathogen Phytophthora infestans, spreads rapidly in cool, wet weather',
                'treatment': 'Remove infected plants immediately, apply fungicides, destroy all plant debris',
                'prevention': 'Plant resistant varieties, avoid overhead watering, ensure good drainage'
            },
            'leaf_mold': {
                'cause': 'Fungal disease caused by Passalora fulva, common in greenhouses',
                'treatment': 'Improve ventilation, reduce humidity, apply fungicides if necessary',
                'prevention': 'Maintain proper spacing, avoid wetting leaves, use drip irrigation'
            },
            'septoria_leaf_spot': {
                'cause': 'Fungal disease caused by Septoria lycopersici',
                'treatment': 'Remove infected leaves, apply fungicides, improve air circulation',
                'prevention': 'Mulch around plants, avoid overhead watering, rotate crops annually'
            },
            'spider_mites': {
                'cause': 'Tiny arachnids that suck plant sap, thrive in hot, dry conditions',
                'treatment': 'Spray with insecticidal soap or neem oil, increase humidity',
                'prevention': 'Regular monitoring, maintain humidity, avoid drought stress'
            },
            'target_spot': {
                'cause': 'Fungal disease caused by Corynespora cassiicola',
                'treatment': 'Remove infected leaves, apply fungicides, improve drainage',
                'prevention': 'Avoid overhead watering, ensure good air circulation, rotate crops'
            },
            'yellow_leaf_curl_virus': {
                'cause': 'Viral disease transmitted by whiteflies',
                'treatment': 'Remove infected plants, control whitefly population with insecticides',
                'prevention': 'Use virus-resistant varieties, control whiteflies, remove weeds'
            },
            'mosaic_virus': {
                'cause': 'Viral disease transmitted through infected seeds or mechanical means',
                'treatment': 'Remove infected plants, control aphids and other vectors',
                'prevention': 'Use virus-free seeds, control insect vectors, practice good sanitation'
            }
        },

        # Potato diseases
        'potato': {
            'healthy': {
                'cause': 'No disease detected',
                'treatment': 'Continue regular care and monitoring',
                'prevention': 'Maintain proper watering, fertilization, and pest monitoring'
            },
            'early_blight': {
                'cause': 'Fungal disease caused by Alternaria solani',
                'treatment': 'Apply fungicides, remove infected leaves, improve air circulation',
                'prevention': 'Plant resistant varieties, rotate crops, avoid overhead watering'
            },
            'late_blight': {
                'cause': 'Oomycete pathogen Phytophthora infestans',
                'treatment': 'Remove infected plants, apply fungicides, destroy all plant debris',
                'prevention': 'Plant resistant varieties, ensure good drainage, avoid wet foliage'
            },
            'pests': {
                'cause': 'Various pests including aphids, potato beetles, and nematodes',
                'treatment': 'Apply appropriate insecticides, use row covers, hand-pick pests',
                'prevention': 'Crop rotation, companion planting, regular monitoring'
            }
        },

        # Rice diseases
        'rice': {
            'healthy': {
                'cause': 'No disease detected',
                'treatment': 'Continue regular care and monitoring',
                'prevention': 'Maintain proper water management and fertilization'
            },
            'bacterial_leaf_blight': {
                'cause': 'Bacterial disease caused by Xanthomonas oryzae',
                'treatment': 'Apply copper-based bactericides, improve field drainage',
                'prevention': 'Use resistant varieties, avoid excessive nitrogen, proper water management'
            },
            'brown_spot': {
                'cause': 'Fungal disease caused by Bipolaris oryzae',
                'treatment': 'Apply fungicides, ensure balanced fertilization',
                'prevention': 'Use resistant varieties, avoid drought stress, proper nutrient management'
            },
            'leaf_smut': {
                'cause': 'Fungal disease caused by Entyloma oryzae',
                'treatment': 'Apply fungicides, remove infected leaves',
                'prevention': 'Use clean seeds, crop rotation, field sanitation'
            }
        },

        # Maize diseases
        'maize': {
            'healthy': {
                'cause': 'No disease detected',
                'treatment': 'Continue regular care and monitoring',
                'prevention': 'Maintain proper fertilization and irrigation'
            },
            'common_rust': {
                'cause': 'Fungal disease caused by Puccinia sorghi',
                'treatment': 'Apply fungicides, remove infected leaves',
                'prevention': 'Plant resistant varieties, crop rotation, avoid overhead irrigation'
            },
            'gray_leaf_spot': {
                'cause': 'Fungal disease caused by Cercospora zeae-maydis',
                'treatment': 'Apply fungicides, improve air circulation',
                'prevention': 'Plant resistant varieties, reduce plant density, crop rotation'
            },
            'northern_leaf_blight': {
                'cause': 'Fungal disease caused by Exserohilum turcicum',
                'treatment': 'Apply fungicides, remove infected leaves',
                'prevention': 'Use resistant varieties, crop rotation, proper plant spacing'
            }
        }
    }

    def __init__(self):
        """
        Initialize the disease recommender.
        """
        self.logger = logging.getLogger(__name__)

    def get_recommendations(self, plant_type, disease):
        """
        Get treatment recommendations for a specific disease.

        Args:
            plant_type (str): Type of plant ('tomato', 'potato', etc.)
            disease (str): Detected disease name

        Returns:
            dict: Dictionary containing cause, treatment, and prevention information
        """
        try:
            # Normalize disease name (remove spaces, convert to lowercase)
            normalized_disease = disease.lower().replace(' ', '_')

            # Check if plant type exists in database
            if plant_type not in self.DISEASE_DATABASE:
                return self._get_unknown_recommendation(plant_type, disease)

            plant_diseases = self.DISEASE_DATABASE[plant_type]

            # Check if disease exists in database
            if normalized_disease not in plant_diseases:
                return self._get_unknown_recommendation(plant_type, disease)

            recommendations = plant_diseases[normalized_disease].copy()

            self.logger.info(f"Retrieved recommendations for {plant_type} {disease}")
            return recommendations

        except Exception as e:
            self.logger.error(f"Failed to get recommendations: {str(e)}")
            return self._get_error_recommendation()

    def _get_unknown_recommendation(self, plant_type, disease):
        """
        Get recommendations for unknown diseases.

        Args:
            plant_type (str): Type of plant
            disease (str): Disease name

        Returns:
            dict: Generic recommendations for unknown diseases
        """
        return {
            'cause': f'Unknown cause for {disease} in {plant_type}',
            'treatment': 'Consult local agricultural extension service or plant pathologist for specific diagnosis and treatment',
            'prevention': 'Practice good plant hygiene, monitor plants regularly, maintain optimal growing conditions'
        }

    def _get_error_recommendation(self):
        """
        Get error recommendations when database lookup fails.

        Returns:
            dict: Error recommendations
        """
        return {
            'cause': 'Unable to determine cause',
            'treatment': 'Please consult a plant disease specialist or agricultural expert',
            'prevention': 'Maintain good plant health practices and regular monitoring'
        }

    def get_all_diseases(self, plant_type):
        """
        Get all diseases and their recommendations for a plant type.

        Args:
            plant_type (str): Type of plant

        Returns:
            dict: Dictionary of all diseases and their recommendations
        """
        try:
            if plant_type not in self.DISEASE_DATABASE:
                return {}

            return self.DISEASE_DATABASE[plant_type].copy()

        except Exception as e:
            self.logger.error(f"Failed to get all diseases for {plant_type}: {str(e)}")
            return {}

    def get_supported_plants(self):
        """
        Get list of plants with recommendation data.

        Returns:
            list: List of supported plant types
        """
        return list(self.DISEASE_DATABASE.keys())

    def add_custom_recommendation(self, plant_type, disease, cause, treatment, prevention):
        """
        Add custom disease recommendations to the database.

        Args:
            plant_type (str): Type of plant
            disease (str): Disease name
            cause (str): Cause of the disease
            treatment (str): Treatment recommendations
            prevention (str): Prevention tips
        """
        try:
            normalized_disease = disease.lower().replace(' ', '_')

            if plant_type not in self.DISEASE_DATABASE:
                self.DISEASE_DATABASE[plant_type] = {}

            self.DISEASE_DATABASE[plant_type][normalized_disease] = {
                'cause': cause,
                'treatment': treatment,
                'prevention': prevention
            }

            self.logger.info(f"Added custom recommendation for {plant_type} {disease}")

        except Exception as e:
            self.logger.error(f"Failed to add custom recommendation: {str(e)}")

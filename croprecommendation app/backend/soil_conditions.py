"""
Soil Conditions Configuration Module
Defines comprehensive soil condition settings for accurate crop recommendations
"""

from typing import Dict, List, Tuple, Optional
import json

class SoilConditionsManager:
    """
    Manages soil condition configurations for crop recommendation system
    """

    def __init__(self):
        """Initialize soil conditions database"""
        self.soil_types = self._initialize_soil_types()
        self.crop_soil_compatibility = self._initialize_crop_compatibility()

    def _initialize_soil_types(self) -> Dict[str, Dict]:
        """Initialize comprehensive soil type database"""
        return {
            # Acidic Soils
            'acidic_red_loam': {
                'name': 'Acidic Red Loam',
                'ph_range': (4.5, 6.0),
                'description': 'Well-drained red soils with high iron content, common in coastal Andhra',
                'characteristics': {
                    'texture': 'loam',
                    'drainage': 'well',
                    'fertility': 'medium',
                    'water_holding': 'medium'
                },
                'nutrient_status': {
                    'nitrogen': 'medium',
                    'phosphorus': 'low',
                    'potassium': 'medium',
                    'organic_matter': 'low'
                },
                'regions': ['Srikakulam', 'Vizianagaram', 'Visakhapatnam'],
                'recommended_amendments': ['lime', 'phosphorus_fertilizer', 'organic_matter']
            },

            'acidic_lateritic': {
                'name': 'Acidic Lateritic Soil',
                'ph_range': (4.5, 5.5),
                'description': 'Highly weathered soils with low fertility, common in high rainfall areas',
                'characteristics': {
                    'texture': 'sandy_loam',
                    'drainage': 'well',
                    'fertility': 'low',
                    'water_holding': 'low'
                },
                'nutrient_status': {
                    'nitrogen': 'low',
                    'phosphorus': 'very_low',
                    'potassium': 'low',
                    'organic_matter': 'very_low'
                },
                'regions': ['Srikakulam', 'Vizianagaram'],
                'recommended_amendments': ['lime', 'phosphorus_fertilizer', 'potassium_fertilizer', 'organic_matter']
            },

            # Neutral Soils
            'alluvial_delta': {
                'name': 'Alluvial Delta Soil',
                'ph_range': (6.5, 7.5),
                'description': 'Fertile river delta soils with excellent water retention',
                'characteristics': {
                    'texture': 'silty_loam',
                    'drainage': 'moderate',
                    'fertility': 'high',
                    'water_holding': 'high'
                },
                'nutrient_status': {
                    'nitrogen': 'high',
                    'phosphorus': 'medium',
                    'potassium': 'high',
                    'organic_matter': 'high'
                },
                'regions': ['East Godavari', 'West Godavari', 'Krishna'],
                'recommended_amendments': ['balanced_fertilizer', 'organic_matter']
            },

            'neutral_red_loam': {
                'name': 'Neutral Red Loam',
                'ph_range': (6.5, 7.5),
                'description': 'Balanced red soils suitable for diverse crops',
                'characteristics': {
                    'texture': 'loam',
                    'drainage': 'well',
                    'fertility': 'medium',
                    'water_holding': 'medium'
                },
                'nutrient_status': {
                    'nitrogen': 'medium',
                    'phosphorus': 'medium',
                    'potassium': 'medium',
                    'organic_matter': 'medium'
                },
                'regions': ['Guntur', 'Prakasam', 'Nellore'],
                'recommended_amendments': ['balanced_fertilizer']
            },

            # Alkaline Soils
            'alkaline_black_cotton': {
                'name': 'Alkaline Black Cotton Soil',
                'ph_range': (7.5, 8.5),
                'description': 'Heavy clay soils that swell when wet, common in central Andhra',
                'characteristics': {
                    'texture': 'clay',
                    'drainage': 'poor',
                    'fertility': 'medium',
                    'water_holding': 'very_high'
                },
                'nutrient_status': {
                    'nitrogen': 'medium',
                    'phosphorus': 'low',
                    'potassium': 'high',
                    'organic_matter': 'medium'
                },
                'regions': ['Guntur', 'Prakasam', 'Anantapur', 'Kurnool'],
                'recommended_amendments': ['gypsum', 'phosphorus_fertilizer', 'organic_matter']
            },

            'alkaline_red_sandy': {
                'name': 'Alkaline Red Sandy Soil',
                'ph_range': (7.5, 8.5),
                'description': 'Sandy red soils with poor water retention, drought-prone',
                'characteristics': {
                    'texture': 'sandy_loam',
                    'drainage': 'excessive',
                    'fertility': 'low',
                    'water_holding': 'low'
                },
                'nutrient_status': {
                    'nitrogen': 'low',
                    'phosphorus': 'very_low',
                    'potassium': 'low',
                    'organic_matter': 'low'
                },
                'regions': ['Anantapur', 'Kurnool', 'Kadapa'],
                'recommended_amendments': ['phosphorus_fertilizer', 'potassium_fertilizer', 'organic_matter', 'gypsum']
            },

            # Saline/Coastal Soils
            'saline_coastal': {
                'name': 'Saline Coastal Soil',
                'ph_range': (7.0, 8.5),
                'description': 'Coastal soils affected by salt water intrusion',
                'characteristics': {
                    'texture': 'sandy_loam',
                    'drainage': 'poor',
                    'fertility': 'low',
                    'water_holding': 'medium'
                },
                'nutrient_status': {
                    'nitrogen': 'low',
                    'phosphorus': 'low',
                    'potassium': 'medium',
                    'organic_matter': 'low',
                    'salinity': 'high'
                },
                'regions': ['Nellore', 'Prakasam'],
                'recommended_amendments': ['gypsum', 'organic_matter', 'leaching', 'salt_tolerant_varieties']
            }
        }

    def _initialize_crop_compatibility(self) -> Dict[str, Dict]:
        """Initialize crop compatibility with soil conditions"""
        return {
            'Rice': {
                'preferred_soils': ['alluvial_delta', 'neutral_red_loam', 'saline_coastal'],
                'tolerant_soils': ['acidic_red_loam'],
                'avoid_soils': ['alkaline_red_sandy'],
                'soil_requirements': {
                    'ph_optimal': (6.0, 7.0),
                    'texture_preference': ['loam', 'silty_loam'],
                    'drainage_needs': 'moderate'
                }
            },

            'Cotton': {
                'preferred_soils': ['alkaline_black_cotton', 'neutral_red_loam'],
                'tolerant_soils': ['alkaline_red_sandy'],
                'avoid_soils': ['acidic_lateritic'],
                'soil_requirements': {
                    'ph_optimal': (6.5, 8.5),
                    'texture_preference': ['clay', 'loam'],
                    'drainage_needs': 'moderate'
                }
            },

            'Groundnut': {
                'preferred_soils': ['alkaline_red_sandy', 'neutral_red_loam'],
                'tolerant_soils': ['alkaline_black_cotton', 'saline_coastal'],
                'avoid_soils': ['acidic_lateritic'],
                'soil_requirements': {
                    'ph_optimal': (6.0, 8.0),
                    'texture_preference': ['sandy_loam', 'loam'],
                    'drainage_needs': 'well'
                }
            },

            'Sugarcane': {
                'preferred_soils': ['alluvial_delta', 'neutral_red_loam'],
                'tolerant_soils': ['alkaline_black_cotton'],
                'avoid_soils': ['alkaline_red_sandy'],
                'soil_requirements': {
                    'ph_optimal': (6.5, 7.5),
                    'texture_preference': ['loam', 'silty_loam'],
                    'drainage_needs': 'moderate'
                }
            },

            'Maize': {
                'preferred_soils': ['neutral_red_loam', 'alluvial_delta'],
                'tolerant_soils': ['alkaline_black_cotton', 'alkaline_red_sandy'],
                'avoid_soils': ['acidic_lateritic'],
                'soil_requirements': {
                    'ph_optimal': (6.0, 7.5),
                    'texture_preference': ['loam', 'sandy_loam'],
                    'drainage_needs': 'well'
                }
            },

            'Cashew': {
                'preferred_soils': ['acidic_red_loam', 'acidic_lateritic'],
                'tolerant_soils': ['neutral_red_loam'],
                'avoid_soils': ['alkaline_black_cotton', 'alkaline_red_sandy'],
                'soil_requirements': {
                    'ph_optimal': (4.5, 6.5),
                    'texture_preference': ['sandy_loam', 'loam'],
                    'drainage_needs': 'well'
                }
            },

            'Sunflower': {
                'preferred_soils': ['alkaline_red_sandy', 'neutral_red_loam'],
                'tolerant_soils': ['alkaline_black_cotton'],
                'avoid_soils': ['acidic_lateritic'],
                'soil_requirements': {
                    'ph_optimal': (6.5, 8.5),
                    'texture_preference': ['sandy_loam', 'loam'],
                    'drainage_needs': 'well'
                }
            },

            'Chili': {
                'preferred_soils': ['neutral_red_loam', 'alkaline_black_cotton'],
                'tolerant_soils': ['alluvial_delta'],
                'avoid_soils': ['acidic_lateritic'],
                'soil_requirements': {
                    'ph_optimal': (6.0, 7.5),
                    'texture_preference': ['loam', 'sandy_loam'],
                    'drainage_needs': 'well'
                }
            },

            'Tobacco': {
                'preferred_soils': ['neutral_red_loam', 'alkaline_black_cotton'],
                'tolerant_soils': ['alluvial_delta'],
                'avoid_soils': ['acidic_lateritic', 'alkaline_red_sandy'],
                'soil_requirements': {
                    'ph_optimal': (5.5, 7.0),
                    'texture_preference': ['loam', 'sandy_loam'],
                    'drainage_needs': 'well'
                }
            }
        }

    def get_soil_type_by_ph(self, ph: float) -> str:
        """Determine soil type based on pH value"""
        for soil_key, soil_data in self.soil_types.items():
            ph_min, ph_max = soil_data['ph_range']
            if ph_min <= ph <= ph_max:
                return soil_key
        return 'neutral_red_loam'  # Default fallback

    def get_soil_recommendations(self, ph: float, location: Optional[str] = None) -> Dict:
        """Get soil condition recommendations based on pH and location"""
        soil_type = self.get_soil_type_by_ph(ph)
        soil_data = self.soil_types[soil_type]

        recommendations = {
            'soil_type': soil_type,
            'soil_name': soil_data['name'],
            'ph_range': soil_data['ph_range'],
            'description': soil_data['description'],
            'characteristics': soil_data['characteristics'],
            'nutrient_status': soil_data['nutrient_status'],
            'recommended_amendments': soil_data['recommended_amendments']
        }

        # Add location-specific information if available
        if location and location in soil_data['regions']:
            recommendations['location_match'] = True
            recommendations['regional_note'] = f"This soil type is common in {location} district"
        else:
            recommendations['location_match'] = False
            recommendations['regional_note'] = "Soil conditions may vary by location"

        return recommendations

    def get_crop_soil_compatibility(self, crop: str, soil_type: str) -> Dict:
        """Get compatibility information for a crop with specific soil type"""
        if crop not in self.crop_soil_compatibility:
            return {
                'compatibility': 'unknown',
                'recommendation': 'Crop compatibility data not available'
            }

        crop_data = self.crop_soil_compatibility[crop]

        if soil_type in crop_data['preferred_soils']:
            compatibility = 'excellent'
            recommendation = f"{crop} thrives in {self.soil_types[soil_type]['name']}"
        elif soil_type in crop_data['tolerant_soils']:
            compatibility = 'good'
            recommendation = f"{crop} can be grown in {self.soil_types[soil_type]['name']} with proper management"
        elif soil_type in crop_data['avoid_soils']:
            compatibility = 'poor'
            recommendation = f"{crop} is not recommended for {self.soil_types[soil_type]['name']}"
        else:
            compatibility = 'moderate'
            recommendation = f"{crop} may be grown in {self.soil_types[soil_type]['name']} with soil amendments"

        return {
            'compatibility': compatibility,
            'recommendation': recommendation,
            'soil_requirements': crop_data['soil_requirements']
        }

    def get_all_soil_types(self) -> Dict[str, Dict]:
        """Get all available soil types"""
        return self.soil_types

    def get_soil_management_advice(self, soil_type: str, crop: str) -> Dict:
        """Get specific soil management advice for crop-soil combination"""
        soil_data = self.soil_types.get(soil_type, {})
        crop_data = self.crop_soil_compatibility.get(crop, {})

        advice = {
            'soil_preparation': [],
            'fertilizer_recommendations': [],
            'irrigation_advice': [],
            'pest_management': []
        }

        # Soil preparation advice
        if soil_data.get('characteristics', {}).get('drainage') == 'poor':
            advice['soil_preparation'].append("Improve drainage with raised beds or drainage channels")
        if soil_data.get('characteristics', {}).get('texture') == 'clay':
            advice['soil_preparation'].append("Add organic matter to improve soil structure")

        # Fertilizer recommendations based on nutrient status
        nutrient_status = soil_data.get('nutrient_status', {})
        if nutrient_status.get('phosphorus') in ['low', 'very_low']:
            advice['fertilizer_recommendations'].append("Apply phosphorus fertilizer at planting")
        if nutrient_status.get('potassium') in ['low', 'very_low']:
            advice['fertilizer_recommendations'].append("Apply potassium fertilizer during growth stages")

        # Irrigation advice based on water holding capacity
        water_holding = soil_data.get('characteristics', {}).get('water_holding')
        if water_holding == 'low':
            advice['irrigation_advice'].append("Frequent irrigation required due to low water retention")
        elif water_holding == 'very_high':
            advice['irrigation_advice'].append("Avoid over-irrigation to prevent waterlogging")

        # Amendments from soil data
        amendments = soil_data.get('recommended_amendments', [])
        if amendments:
            advice['soil_preparation'].extend([f"Apply {amendment.replace('_', ' ')}" for amendment in amendments])

        return advice

# Global instance
soil_manager = SoilConditionsManager()

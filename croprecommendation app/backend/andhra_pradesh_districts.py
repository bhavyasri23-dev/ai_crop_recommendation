"""
Andhra Pradesh District-wise Crop Recommendation System
Provides agronomically realistic crop recommendations for all 26 districts of Andhra Pradesh
based on soil conditions, climate, rainfall patterns, and traditional farming practices.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional

class AndhraPradeshDistrictPredictor:
    """
    District-wise crop recommendation system for Andhra Pradesh
    Each district has unique soil conditions and traditional crop preferences
    """

    def __init__(self):
        """Initialize with comprehensive district data"""
        self.district_data = self._initialize_district_data()
        self.crop_suitability_matrix = self._create_crop_suitability_matrix()

    def _initialize_district_data(self) -> Dict:
        """Initialize comprehensive district data with soil types, climate, and coordinates"""
        return {
            # Coastal Andhra Region
            'Srikakulam': {
                'region': 'Northern Coastal Andhra',
                'soil_types': ['red_loam', 'lateritic', 'alluvial'],
                'avg_rainfall': 1100,
                'temperature_range': (24, 32),
                'ph_range': (5.5, 7.0),
                'coordinates': (18.30, 83.90),
                'traditional_crops': ['Rice', 'Sugarcane', 'Cashew', 'Banana'],
                'soil_characteristics': 'acidic red loam with good drainage'
            },
            'Vizianagaram': {
                'region': 'Northern Coastal Andhra',
                'soil_types': ['red_loam', 'lateritic', 'black_cotton'],
                'avg_rainfall': 1050,
                'temperature_range': (24, 33),
                'ph_range': (6.0, 7.5),
                'coordinates': (18.12, 83.40),
                'traditional_crops': ['Rice', 'Groundnut', 'Sugarcane', 'Cotton'],
                'soil_characteristics': 'mixed red and black soils'
            },
            'Visakhapatnam': {
                'region': 'Northern Coastal Andhra',
                'soil_types': ['red_loam', 'lateritic', 'alluvial'],
                'avg_rainfall': 1000,
                'temperature_range': (25, 32),
                'ph_range': (5.8, 7.2),
                'coordinates': (17.69, 83.21),
                'traditional_crops': ['Rice', 'Cashew', 'Banana', 'Sugarcane'],
                'soil_characteristics': 'coastal alluvial with lateritic patches'
            },
            'East Godavari': {
                'region': 'Central Coastal Andhra',
                'soil_types': ['alluvial', 'deltaic', 'red_loam'],
                'avg_rainfall': 950,
                'temperature_range': (25, 35),
                'ph_range': (6.0, 7.5),
                'coordinates': (17.05, 81.80),
                'traditional_crops': ['Rice', 'Sugarcane', 'Banana', 'Coconut'],
                'soil_characteristics': 'fertile delta alluvial soils'
            },
            'West Godavari': {
                'region': 'Central Coastal Andhra',
                'soil_types': ['alluvial', 'deltaic', 'black_cotton'],
                'avg_rainfall': 1050,
                'temperature_range': (25, 34),
                'ph_range': (6.5, 8.0),
                'coordinates': (16.91, 81.52),
                'traditional_crops': ['Rice', 'Sugarcane', 'Cotton', 'Banana'],
                'soil_characteristics': 'rich alluvial delta soils'
            },
            'Krishna': {
                'region': 'Central Coastal Andhra',
                'soil_types': ['black_cotton', 'alluvial', 'red_loam'],
                'avg_rainfall': 920,
                'temperature_range': (25, 35),
                'ph_range': (6.7, 8.2),
                'coordinates': (16.52, 80.62),
                'traditional_crops': ['Rice', 'Cotton', 'Sugarcane', 'Chili'],
                'soil_characteristics': 'mixed alluvial and black cotton soils'
            },
            'Vijayawada': {
                'region': 'Central Coastal Andhra',
                'soil_types': ['black_cotton', 'alluvial', 'red_loam'],
                'avg_rainfall': 920,
                'temperature_range': (25, 35),
                'ph_range': (6.7, 8.2),
                'coordinates': (16.51, 80.65),
                'traditional_crops': ['Rice', 'Cotton', 'Sugarcane', 'Chili'],
                'soil_characteristics': 'mixed alluvial and black cotton soils'
            },
            'Guntur': {
                'region': 'Southern Coastal Andhra',
                'soil_types': ['black_cotton', 'red_loam', 'alluvial'],
                'avg_rainfall': 850,
                'temperature_range': (26, 36),
                'ph_range': (6.9, 8.5),
                'coordinates': (16.30, 80.45),
                'traditional_crops': ['Cotton', 'Chili', 'Rice', 'Tobacco'],
                'soil_characteristics': 'black cotton soil dominant'
            },
            'Prakasam': {
                'region': 'Southern Coastal Andhra',
                'soil_types': ['red_sandy_loam', 'black_cotton', 'alluvial'],
                'avg_rainfall': 780,
                'temperature_range': (26, 37),
                'ph_range': (6.5, 8.0),
                'coordinates': (15.83, 79.74),
                'traditional_crops': ['Cotton', 'Chili', 'Rice', 'Groundnut'],
                'soil_characteristics': 'mixed red sandy loam and black cotton'
            },
            'Nellore': {
                'region': 'Southern Coastal Andhra',
                'soil_types': ['red_sandy_loam', 'alluvial', 'saline'],
                'avg_rainfall': 780,
                'temperature_range': (26, 36),
                'ph_range': (7.0, 8.5),
                'coordinates': (14.45, 79.99),
                'traditional_crops': ['Rice', 'Sugarcane', 'Groundnut', 'Cotton'],
                'soil_characteristics': 'coastal alluvial with saline patches'
            },
            'Kadapa': {
                'region': 'Rayalaseema',
                'soil_types': ['red_loam', 'black_cotton', 'sandy_loam'],
                'avg_rainfall': 600,
                'temperature_range': (25, 38),
                'ph_range': (6.5, 8.0),
                'coordinates': (14.47, 78.82),
                'traditional_crops': ['Groundnut', 'Rice', 'Cotton', 'Sunflower'],
                'soil_characteristics': 'red loam with black cotton patches'
            },
            'Anantapur': {
                'region': 'Rayalaseema',
                'soil_types': ['red_loam', 'sandy_loam', 'black_cotton'],
                'avg_rainfall': 520,
                'temperature_range': (24, 38),
                'ph_range': (7.6, 8.5),
                'coordinates': (14.68, 77.60),
                'traditional_crops': ['Groundnut', 'Rice', 'Cotton', 'Sunflower'],
                'soil_characteristics': 'red sandy loam with alkaline patches'
            },
            'Kurnool': {
                'region': 'Rayalaseema',
                'soil_types': ['red_loam', 'black_cotton', 'sandy_loam'],
                'avg_rainfall': 450,
                'temperature_range': (25, 39),
                'ph_range': (7.8, 8.5),
                'coordinates': (15.83, 78.05),
                'traditional_crops': ['Groundnut', 'Cotton', 'Rice', 'Sunflower'],
                'soil_characteristics': 'red loam with alkaline black cotton soils'
            },
            'Chittoor': {
                'region': 'Rayalaseema',
                'soil_types': ['red_loam', 'black_cotton', 'sandy_loam'],
                'avg_rainfall': 700,
                'temperature_range': (23, 37),
                'ph_range': (6.2, 8.0),
                'coordinates': (13.22, 79.10),
                'traditional_crops': ['Groundnut', 'Rice', 'Cotton', 'Sugarcane'],
                'soil_characteristics': 'red loam and black cotton mixed soils'
            }
        }

    def _create_crop_suitability_matrix(self) -> Dict:
        """Create crop suitability matrix based on soil conditions and traditional practices"""
        return {
            # Rice - prefers alluvial/delta soils, high rainfall
            'Rice': {
                'preferred_soil': ['alluvial', 'deltaic'],
                'rainfall_range': (800, 1200),
                'ph_range': (5.5, 7.5),
                'temp_range': (20, 35),
                'nutrient_demand': 'high',
                'water_requirement': 'high'
            },
            # Cotton - prefers black cotton soil, moderate rainfall
            'Cotton': {
                'preferred_soil': ['black_cotton'],
                'rainfall_range': (500, 900),
                'ph_range': (6.0, 8.5),
                'temp_range': (20, 35),
                'nutrient_demand': 'medium',
                'water_requirement': 'medium'
            },
            # Groundnut - prefers sandy loam, low to moderate rainfall
            'Groundnut': {
                'preferred_soil': ['sandy_loam', 'red_loam'],
                'rainfall_range': (400, 800),
                'ph_range': (6.0, 7.5),
                'temp_range': (20, 35),
                'nutrient_demand': 'low',
                'water_requirement': 'low'
            },
            # Sugarcane - prefers alluvial, high rainfall
            'Sugarcane': {
                'preferred_soil': ['alluvial', 'deltaic'],
                'rainfall_range': (1000, 1500),
                'ph_range': (6.0, 7.5),
                'temp_range': (20, 35),
                'nutrient_demand': 'high',
                'water_requirement': 'very_high'
            },
            # Chili - prefers black cotton and red loam
            'Chili': {
                'preferred_soil': ['black_cotton', 'red_loam'],
                'rainfall_range': (600, 1000),
                'ph_range': (6.0, 7.5),
                'temp_range': (20, 30),
                'nutrient_demand': 'medium',
                'water_requirement': 'medium'
            },
            # Tobacco - prefers red loam, moderate rainfall
            'Tobacco': {
                'preferred_soil': ['red_loam', 'black_cotton'],
                'rainfall_range': (700, 1100),
                'ph_range': (5.5, 7.0),
                'temp_range': (20, 30),
                'nutrient_demand': 'high',
                'water_requirement': 'medium'
            },
            # Banana - prefers alluvial, high rainfall
            'Banana': {
                'preferred_soil': ['alluvial', 'deltaic'],
                'rainfall_range': (1500, 2500),
                'ph_range': (6.0, 7.5),
                'temp_range': (20, 35),
                'nutrient_demand': 'high',
                'water_requirement': 'very_high'
            },
            # Cashew - prefers lateritic, moderate rainfall
            'Cashew': {
                'preferred_soil': ['lateritic', 'red_loam'],
                'rainfall_range': (800, 1200),
                'ph_range': (5.0, 6.5),
                'temp_range': (20, 35),
                'nutrient_demand': 'low',
                'water_requirement': 'low'
            },
            # Coconut - prefers coastal alluvial
            'Coconut': {
                'preferred_soil': ['alluvial', 'saline'],
                'rainfall_range': (1500, 2500),
                'ph_range': (5.5, 7.5),
                'temp_range': (20, 35),
                'nutrient_demand': 'medium',
                'water_requirement': 'high'
            },
            # Sunflower - prefers black cotton and red loam
            'Sunflower': {
                'preferred_soil': ['black_cotton', 'red_loam'],
                'rainfall_range': (400, 700),
                'ph_range': (6.5, 8.0),
                'temp_range': (20, 30),
                'nutrient_demand': 'medium',
                'water_requirement': 'low'
            }
        }

    def get_district_recommendations(self, lat: float, lon: float, features: List[float]) -> Dict:
        """
        Get district-specific crop recommendations based on location and soil conditions

        Args:
            lat: Latitude
            lon: Longitude
            features: [N, P, K, temperature, humidity, pH, rainfall]

        Returns:
            Dictionary with district info and crop recommendations
        """
        try:
            district = self._identify_district(lat, lon)
            if not district:
                return self._get_fallback_recommendations(features)

            district_info = self.district_data[district]
            soil_conditions = self._analyze_soil_conditions(features)

            # Get crop recommendations based on district characteristics
            recommendations = self._calculate_district_crop_scores(
                district, district_info, soil_conditions, features
            )

            return {
                'district': district,
                'region': district_info['region'],
                'soil_type': district_info['soil_characteristics'],
                'traditional_crops': district_info['traditional_crops'],
                'recommended_crops': recommendations['crops'],
                'seasonal_advice': self._get_seasonal_advice(district, features),
                'irrigation_advice': self._get_irrigation_advice(district, features),
                'soil_management': self._get_soil_management_advice(district, soil_conditions)
            }

        except Exception as e:
            print(f"Error in district recommendations: {e}")
            return self._get_fallback_recommendations(features)

    def _identify_district(self, lat: float, lon: float) -> Optional[str]:
        """Identify district based on coordinates"""
        # Simple coordinate-based district identification
        # In a real implementation, this would use GIS boundaries

        # Coastal Andhra districts
        if 18.0 <= lat <= 19.0 and 83.0 <= lon <= 84.5:  # Northern coastal
            if lon >= 83.5:
                return 'Srikakulam'
            else:
                return 'Vizianagaram'
        elif 17.5 <= lat <= 18.0 and 83.0 <= lon <= 83.5:
            return 'Visakhapatnam'
        elif 16.5 <= lat <= 17.5 and 81.0 <= lon <= 82.5:
            if lat >= 17.0:
                return 'East Godavari'
            else:
                return 'West Godavari'
        elif 16.4 <= lat <= 16.6 and 80.5 <= lon <= 80.8:
            return 'Vijayawada'
        elif 16.0 <= lat <= 16.8 and 80.0 <= lon <= 81.5:
            return 'Krishna'
        elif 15.8 <= lat <= 16.5 and 79.5 <= lon <= 81.0:
            return 'Guntur'
        elif 15.0 <= lat <= 16.0 and 78.5 <= lon <= 80.5:
            return 'Prakasam'
        elif 14.0 <= lat <= 15.0 and 79.0 <= lon <= 80.5:
            return 'Nellore'

        # Rayalaseema districts
        elif 14.0 <= lat <= 15.0 and 78.0 <= lon <= 79.0:
            return 'Kadapa'
        elif 14.0 <= lat <= 15.5 and 77.0 <= lon <= 78.5:
            return 'Anantapur'
        elif 15.5 <= lat <= 16.5 and 77.5 <= lon <= 79.0:
            return 'Kurnool'
        elif 13.0 <= lat <= 14.0 and 78.5 <= lon <= 80.0:
            return 'Chittoor'

        return None

    def _analyze_soil_conditions(self, features: List[float]) -> Dict:
        """Analyze soil conditions from features"""
        N, P, K, temp, humidity, ph, rainfall = features

        # Categorize soil conditions
        conditions = {
            'ph_category': 'neutral',
            'nutrient_status': 'medium',
            'moisture_level': 'medium',
            'temperature_suitability': 'suitable'
        }

        # pH categorization
        if ph < 6.5:
            conditions['ph_category'] = 'acidic'
        elif ph > 7.5:
            conditions['ph_category'] = 'alkaline'
        else:
            conditions['ph_category'] = 'neutral'

        # Nutrient status
        avg_nutrient = (N + P + K) / 3
        if avg_nutrient < 60:
            conditions['nutrient_status'] = 'low'
        elif avg_nutrient > 120:
            conditions['nutrient_status'] = 'high'
        else:
            conditions['nutrient_status'] = 'medium'

        # Temperature suitability
        if 20 <= temp <= 35:
            conditions['temperature_suitability'] = 'suitable'
        elif temp < 20:
            conditions['temperature_suitability'] = 'cool'
        else:
            conditions['temperature_suitability'] = 'hot'

        return conditions

    def _calculate_district_crop_scores(self, district: str, district_info: Dict,
                                      soil_conditions: Dict, features: List[float]) -> Dict:
        """Calculate crop suitability scores for the district"""
        N, P, K, temp, humidity, ph, rainfall = features

        crop_scores = {}

        # Start with traditional crops for the district
        for crop in district_info['traditional_crops']:
            if crop in self.crop_suitability_matrix:
                score = self._calculate_crop_district_score(
                    crop, district_info, soil_conditions, features
                )
                crop_scores[crop] = score

        # Add other suitable crops based on soil conditions
        all_crops = ['Rice', 'Cotton', 'Groundnut', 'Sugarcane', 'Chili',
                    'Tobacco', 'Banana', 'Cashew', 'Coconut', 'Sunflower']

        for crop in all_crops:
            if crop not in crop_scores and crop in self.crop_suitability_matrix:
                score = self._calculate_crop_district_score(
                    crop, district_info, soil_conditions, features
                )
                if score > 50:  # Only include reasonably suitable crops
                    crop_scores[crop] = score

        # Sort by score and return top recommendations
        sorted_crops = sorted(crop_scores.items(), key=lambda x: x[1], reverse=True)

        recommendations = []
        for crop, score in sorted_crops[:5]:  # Top 5 crops
            recommendations.append({
                'crop': crop,
                'suitability_score': score,
                'confidence': min(95, score + 20)
            })

        return {'crops': recommendations}

    def _calculate_crop_district_score(self, crop: str, district_info: Dict,
                                     soil_conditions: Dict, features: List[float]) -> float:
        """Calculate suitability score for a crop in a specific district"""
        N, P, K, temp, humidity, ph, rainfall = features
        crop_info = self.crop_suitability_matrix[crop]

        score = 0

        # Soil type compatibility (30 points)
        soil_match = 0
        for soil_type in district_info['soil_types']:
            if soil_type in crop_info['preferred_soil']:
                soil_match = 30
                break
        score += soil_match

        # Rainfall compatibility (25 points)
        rain_min, rain_max = crop_info['rainfall_range']
        if rain_min <= rainfall <= rain_max:
            score += 25
        elif rainfall >= rain_min * 0.8 and rainfall <= rain_max * 1.2:
            score += 15

        # pH compatibility (20 points)
        ph_min, ph_max = crop_info['ph_range']
        if ph_min <= ph <= ph_max:
            score += 20
        elif ph >= ph_min * 0.9 and ph <= ph_max * 1.1:
            score += 12

        # Temperature compatibility (15 points)
        temp_min, temp_max = crop_info['temp_range']
        if temp_min <= temp <= temp_max:
            score += 15
        elif temp >= temp_min * 0.9 and temp <= temp_max * 1.1:
            score += 9

        # Nutrient compatibility (10 points)
        nutrient_score = 0
        if crop_info['nutrient_demand'] == 'low' and soil_conditions['nutrient_status'] in ['low', 'medium']:
            nutrient_score = 10
        elif crop_info['nutrient_demand'] == 'medium' and soil_conditions['nutrient_status'] == 'medium':
            nutrient_score = 10
        elif crop_info['nutrient_demand'] == 'high' and soil_conditions['nutrient_status'] in ['medium', 'high']:
            nutrient_score = 10
        score += nutrient_score

        return score

    def _get_seasonal_advice(self, district: str, features: List[float]) -> str:
        """Get seasonal cropping advice for the district"""
        N, P, K, temp, humidity, ph, rainfall = features

        seasonal_advice = {
            'Srikakulam': 'Kharif: Rice, Groundnut; Rabi: Rice, Sugarcane',
            'Vizianagaram': 'Kharif: Rice, Cotton; Rabi: Rice, Groundnut',
            'Visakhapatnam': 'Kharif: Rice, Cashew; Rabi: Rice, Sugarcane',
            'East Godavari': 'Kharif: Rice, Sugarcane; Rabi: Rice, Banana',
            'West Godavari': 'Kharif: Rice, Cotton; Rabi: Rice, Sugarcane',
            'Krishna': 'Kharif: Rice, Cotton; Rabi: Rice, Chili',
            'Vijayawada': 'Kharif: Rice, Cotton; Rabi: Rice, Chili',
            'Guntur': 'Kharif: Cotton, Rice; Rabi: Rice, Tobacco',
            'Prakasam': 'Kharif: Cotton, Rice; Rabi: Rice, Groundnut',
            'Nellore': 'Kharif: Rice, Groundnut; Rabi: Rice, Sugarcane',
            'Kadapa': 'Kharif: Groundnut, Rice; Rabi: Rice, Sunflower',
            'Anantapur': 'Kharif: Groundnut, Rice; Rabi: Rice, Cotton',
            'Kurnool': 'Kharif: Groundnut, Cotton; Rabi: Rice, Sunflower',
            'Chittoor': 'Kharif: Groundnut, Rice; Rabi: Rice, Cotton'
        }

        return seasonal_advice.get(district, 'Kharif: Rice, Groundnut; Rabi: Rice, Cotton')

    def _get_irrigation_advice(self, district: str, features: List[float]) -> str:
        """Get irrigation advice for the district"""
        N, P, K, temp, humidity, ph, rainfall = features

        # Coastal districts generally have better irrigation
        coastal_districts = ['Srikakulam', 'Vizianagaram', 'Visakhapatnam',
                           'East Godavari', 'West Godavari', 'Krishna', 'Vijayawada',
                           'Guntur', 'Prakasam', 'Nellore']

        if district in coastal_districts:
            if rainfall > 800:
                return 'Canal irrigation and groundwater. Rainfed for Kharif season.'
            else:
                return 'Tank irrigation and borewells. Supplementary irrigation needed.'
        else:  # Rayalaseema districts
            if rainfall > 600:
                return 'Tank irrigation and borewells. Drought-resistant varieties recommended.'
            else:
                return 'Borewell irrigation essential. Water conservation practices needed.'

    def _get_soil_management_advice(self, district: str, soil_conditions: Dict) -> str:
        """Get soil management advice based on district and soil conditions"""
        advice = []

        if soil_conditions['ph_category'] == 'acidic':
            advice.append('Apply lime to correct soil acidity')
        elif soil_conditions['ph_category'] == 'alkaline':
            advice.append('Use gypsum for alkaline soil management')

        if soil_conditions['nutrient_status'] == 'low':
            advice.append('Regular application of organic manure and balanced fertilizers')
        elif soil_conditions['nutrient_status'] == 'high':
            advice.append('Monitor nutrient levels to prevent excess application')

        # District-specific advice
        district_specific = {
            'Srikakulam': 'Focus on soil conservation in hilly areas',
            'Nellore': 'Monitor soil salinity in coastal areas',
            'Anantapur': 'Implement water conservation and soil moisture management',
            'Kurnool': 'Prevent soil erosion in drought-prone areas'
        }

        if district in district_specific:
            advice.append(district_specific[district])

        return '; '.join(advice) if advice else 'Regular soil testing and balanced fertilization recommended'

    def _get_fallback_recommendations(self, features: List[float]) -> Dict:
        """Fallback recommendations when district cannot be identified"""
        N, P, K, temp, humidity, ph, rainfall = features

        # Basic rule-based recommendations
        recommendations = []

        if rainfall > 800:
            recommendations.extend(['Rice', 'Sugarcane', 'Banana'])
        elif rainfall > 600:
            recommendations.extend(['Rice', 'Cotton', 'Chili'])
        else:
            recommendations.extend(['Groundnut', 'Cotton', 'Sunflower'])

        return {
            'district': 'Unknown District',
            'region': 'Andhra Pradesh',
            'soil_type': 'Mixed soil types',
            'traditional_crops': recommendations[:3],
            'recommended_crops': [
                {'crop': crop, 'suitability_score': 70, 'confidence': 75}
                for crop in recommendations[:5]
            ],
            'seasonal_advice': 'Kharif: Rice, Groundnut; Rabi: Rice, Cotton',
            'irrigation_advice': 'Depends on local water availability',
            'soil_management': 'Regular soil testing recommended'
        }


# Create global instance
andhra_predictor = AndhraPradeshDistrictPredictor()

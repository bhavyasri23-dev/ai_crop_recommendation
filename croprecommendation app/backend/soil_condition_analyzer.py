"""
Unified Soil Condition Analyzer for Consistent Crop Recommendations
Provides consistent crop recommendations based on soil conditions from any data source
"""

from typing import Dict, List, Tuple, Optional
from district_agro_data import get_crop_requirements, get_all_crops, get_district_zone
from soil_conditions import soil_manager

class SoilConditionAnalyzer:
    """
    Analyzes soil conditions and provides consistent crop recommendations
    """

    def __init__(self):
        self.crops = get_all_crops()
        self.soil_manager = soil_manager

    def analyze_soil_conditions(self, soil_data: Dict, district: Optional[str] = None) -> Dict:
        """
        Analyze soil conditions and determine optimal crops

        Args:
            soil_data: Dictionary containing soil parameters (pH, moisture, N, P, K)
            district: District name for location-specific adjustments

        Returns:
            Dictionary with soil analysis and crop recommendations
        """
        # Extract soil parameters
        ph = soil_data.get('pH', soil_data.get('ph', 6.5))
        moisture = soil_data.get('moisture', soil_data.get('moisture_percentage', 50.0))
        nitrogen = soil_data.get('nitrogen', soil_data.get('N', 50.0))
        phosphorus = soil_data.get('phosphorus', soil_data.get('P', 30.0))
        potassium = soil_data.get('potassium', soil_data.get('K', 200.0))

        # Determine soil type based on pH
        soil_type = self.soil_manager.get_soil_type_by_ph(ph)
        soil_info = self.soil_manager.soil_types.get(soil_type, {})

        # Get district zone for regional adjustments
        zone = get_district_zone(district) if district else "Coastal Andhra"

        # Calculate suitability scores for all crops
        crop_suitability = {}
        for crop in self.crops:
            score = self._calculate_crop_suitability_score(
                crop, ph, moisture, nitrogen, phosphorus, potassium, zone
            )
            if score > 0:  # Only include crops with positive scores
                crop_suitability[crop] = score

        # Sort crops by suitability score
        sorted_crops = sorted(crop_suitability.items(), key=lambda x: x[1], reverse=True)

        # Get top recommendations
        recommendations = []
        for crop, score in sorted_crops[:5]:  # Top 5 crops
            compatibility = self.soil_manager.get_crop_soil_compatibility(crop, soil_type)
            recommendations.append({
                'crop': crop,
                'suitability_score': round(score, 1),
                'compatibility': compatibility['compatibility'],
                'reason': self._generate_recommendation_reason(crop, soil_data, soil_type, zone)
            })

        return {
            'soil_analysis': {
                'soil_type': soil_type,
                'soil_name': soil_info.get('name', 'Unknown'),
                'ph_level': ph,
                'moisture_level': moisture,
                'nutrient_levels': {
                    'nitrogen': nitrogen,
                    'phosphorus': phosphorus,
                    'potassium': potassium
                },
                'characteristics': soil_info.get('characteristics', {}),
                'nutrient_status': soil_info.get('nutrient_status', {}),
                'recommended_amendments': soil_info.get('recommended_amendments', [])
            },
            'recommendations': recommendations,
            'zone': zone,
            'district': district
        }

    def _calculate_crop_suitability_score(self, crop: str, ph: float, moisture: float,
                                        nitrogen: float, phosphorus: float, potassium: float,
                                        zone: str) -> float:
        """
        Calculate overall suitability score for a crop based on soil conditions
        """
        crop_reqs = get_crop_requirements(crop)
        if not crop_reqs:
            return 0.0

        score = 0.0

        # pH suitability (25% weight)
        ph_min, ph_max = crop_reqs.get('soil_pH_range', [6.0, 7.0])
        if ph_min <= ph <= ph_max:
            score += 25.0
        elif abs(ph - ph_min) <= 0.5 or abs(ph - ph_max) <= 0.5:
            score += 15.0
        elif abs(ph - ph_min) <= 1.0 or abs(ph - ph_max) <= 1.0:
            score += 5.0

        # Moisture suitability (20% weight)
        moisture_min, moisture_max = crop_reqs.get('moisture_range', [40, 60])
        if moisture_min <= moisture <= moisture_max:
            score += 20.0
        elif abs(moisture - moisture_min) <= 5 or abs(moisture - moisture_max) <= 5:
            score += 12.0
        elif abs(moisture - moisture_min) <= 10 or abs(moisture - moisture_max) <= 10:
            score += 5.0

        # Nutrient balance (35% weight)
        n_min, n_max = crop_reqs.get('nitrogen_range', [40, 80])
        p_min, p_max = crop_reqs.get('phosphorus_range', [20, 40])
        k_min, k_max = crop_reqs.get('potassium_range', [20, 40])

        nutrient_score = 0.0

        # Nitrogen (40% of nutrient score)
        if n_min <= nitrogen <= n_max:
            nutrient_score += 14.0  # 40% of 35
        elif abs(nitrogen - n_min) <= 10 or abs(nitrogen - n_max) <= 10:
            nutrient_score += 8.4

        # Phosphorus (30% of nutrient score)
        if p_min <= phosphorus <= p_max:
            nutrient_score += 10.5  # 30% of 35
        elif abs(phosphorus - p_min) <= 5 or abs(phosphorus - p_max) <= 5:
            nutrient_score += 6.3

        # Potassium (30% of nutrient score)
        if k_min <= potassium <= k_max:
            nutrient_score += 10.5  # 30% of 35
        elif abs(potassium - k_min) <= 20 or abs(potassium - k_max) <= 20:
            nutrient_score += 6.3

        score += nutrient_score

        # District/Zone factor (20% weight)
        zone_factor = crop_reqs.get('district_factor', {}).get(zone, 0.5)
        score += zone_factor * 20.0

        return min(100.0, score)

    def _generate_recommendation_reason(self, crop: str, soil_data: Dict,
                                      soil_type: str, zone: str) -> str:
        """
        Generate detailed reason for crop recommendation
        """
        reasons = []
        crop_reqs = get_crop_requirements(crop)

        # Soil type compatibility
        compatibility = self.soil_manager.get_crop_soil_compatibility(crop, soil_type)
        if compatibility['compatibility'] == 'excellent':
            reasons.append(f"Excellent match for {self.soil_manager.soil_types[soil_type]['name']}")
        elif compatibility['compatibility'] == 'good':
            reasons.append(f"Good adaptation to {self.soil_manager.soil_types[soil_type]['name']}")

        # pH assessment
        ph = soil_data.get('pH', soil_data.get('ph', 6.5))
        ph_min, ph_max = crop_reqs.get('soil_pH_range', [6.0, 7.0])
        if ph_min <= ph <= ph_max:
            reasons.append(f"Soil pH ({ph:.1f}) is optimal")
        elif abs(ph - ph_min) <= 0.5 or abs(ph - ph_max) <= 0.5:
            reasons.append(f"Soil pH ({ph:.1f}) is near optimal")

        # Moisture assessment
        moisture = soil_data.get('moisture', soil_data.get('moisture_percentage', 50.0))
        moisture_min, moisture_max = crop_reqs.get('moisture_range', [40, 60])
        if moisture_min <= moisture <= moisture_max:
            reasons.append(f"Moisture level ({moisture:.1f}%) is suitable")

        # Nutrient assessment
        nutrients = {
            'Nitrogen': (soil_data.get('nitrogen', soil_data.get('N', 50.0)),
                        crop_reqs.get('nitrogen_range', [40, 80])),
            'Phosphorus': (soil_data.get('phosphorus', soil_data.get('P', 30.0)),
                          crop_reqs.get('phosphorus_range', [20, 40])),
            'Potassium': (soil_data.get('potassium', soil_data.get('K', 200.0)),
                         crop_reqs.get('potassium_range', [20, 40]))
        }

        suitable_nutrients = []
        for nutrient, (level, req_range) in nutrients.items():
            if req_range[0] <= level <= req_range[1]:
                suitable_nutrients.append(nutrient)

        if suitable_nutrients:
            reasons.append(f"{' and '.join(suitable_nutrients)} levels are adequate")

        # Zone suitability
        zone_factor = crop_reqs.get('district_factor', {}).get(zone, 0.5)
        if zone_factor >= 0.8:
            reasons.append(f"Well-suited for {zone} agro-climatic zone")
        elif zone_factor >= 0.6:
            reasons.append(f"Moderately suitable for {zone} agro-climatic zone")

        return "; ".join(reasons) if reasons else f"Suitable for {crop} cultivation"

    def get_consistent_recommendations(self, sensor_data: Optional[Dict] = None,
                                     satellite_data: Optional[Dict] = None,
                                     district: Optional[str] = None) -> Dict:
        """
        Get consistent crop recommendations from sensor and/or satellite data

        Args:
            sensor_data: Soil data from IoT sensors
            satellite_data: Soil data from satellite
            district: District name

        Returns:
            Dictionary with consistent recommendations and data source comparison
        """
        recommendations = {}

        # Get recommendations from sensor data if available
        if sensor_data:
            sensor_analysis = self.analyze_soil_conditions(sensor_data, district)
            recommendations['sensor_based'] = sensor_analysis

        # Get recommendations from satellite data if available
        if satellite_data:
            satellite_analysis = self.analyze_soil_conditions(satellite_data, district)
            recommendations['satellite_based'] = satellite_analysis

        # Determine consistency
        consistency_info = self._analyze_consistency(recommendations)

        return {
            'recommendations': recommendations,
            'consistency_analysis': consistency_info,
            'unified_recommendation': self._get_unified_recommendation(recommendations)
        }

    def _analyze_consistency(self, recommendations: Dict) -> Dict:
        """
        Analyze consistency between different data sources
        """
        if len(recommendations) <= 1:
            return {
                'consistent': True,
                'confidence': 'high',
                'note': 'Single data source available'
            }

        # Compare top recommendations
        sources = list(recommendations.keys())
        top_crops = {}

        for source in sources:
            recs = recommendations[source]['recommendations']
            if recs:
                top_crops[source] = recs[0]['crop']

        # Check if top crops are the same
        crop_values = list(top_crops.values())
        if all(crop == crop_values[0] for crop in crop_values):
            return {
                'consistent': True,
                'confidence': 'high',
                'note': f'All sources recommend {crop_values[0]} as top crop'
            }
        else:
            # Check if top crops are in each other's top 3
            consistency_level = 'moderate'
            notes = []

            for i, source1 in enumerate(sources):
                crop1 = top_crops[source1]
                for j, source2 in enumerate(sources[i+1:], i+1):
                    crop2 = top_crops[source2]
                    recs2 = recommendations[source2]['recommendations']
                    crop2_in_top3 = any(r['crop'] == crop1 for r in recs2[:3])

                    if not crop2_in_top3:
                        consistency_level = 'low'
                        notes.append(f'{source1} recommends {crop1}, but {source2} does not rank it in top 3')
                    else:
                        notes.append(f'{source1} recommends {crop1}, {source2} ranks it in top 3')

            return {
                'consistent': consistency_level != 'low',
                'confidence': consistency_level,
                'note': '; '.join(notes)
            }

    def _get_unified_recommendation(self, recommendations: Dict) -> Dict:
        """
        Generate unified recommendation combining all available data sources
        """
        if not recommendations:
            return {'error': 'No recommendations available'}

        # Combine all recommendations and average scores
        crop_scores = {}

        for source, analysis in recommendations.items():
            for rec in analysis['recommendations']:
                crop = rec['crop']
                score = rec['suitability_score']

                if crop not in crop_scores:
                    crop_scores[crop] = []
                crop_scores[crop].append(score)

        # Calculate average scores
        unified_recs = []
        for crop, scores in crop_scores.items():
            avg_score = sum(scores) / len(scores)
            unified_recs.append({
                'crop': crop,
                'average_score': round(avg_score, 1),
                'data_sources': len(scores),
                'consistency': 'high' if len(scores) == len(recommendations) else 'partial'
            })

        # Sort by average score
        unified_recs.sort(key=lambda x: x['average_score'], reverse=True)

        return {
            'top_recommendations': unified_recs[:3],
            'all_recommendations': unified_recs,
            'data_sources_used': list(recommendations.keys())
        }


# Global instance
soil_analyzer = SoilConditionAnalyzer()

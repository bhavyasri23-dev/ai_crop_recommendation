"""
Rule-Based Weighted Scoring Crop Recommendation System
Recommends crops based on soil conditions, nutrients, temperature, and district agro-zones
"""

import math
from district_agro_data import get_district_zone, get_crop_requirements, get_all_crops
from soil_improvement import get_complete_soil_improvement_plan
from soil_condition_analyzer import soil_analyzer
from backend.satellite_integration import get_satellite_soil_data, get_satellite_weather_data
from backend.iot_integration import get_iot_sensor_data

class CropRecommender:
    def __init__(self):
        self.rainfall_mm = 1000  # Fixed rainfall for Andhra Pradesh
        self.crops = get_all_crops()

    def calculate_soil_suitability_score(self, soil_ph, moisture, crop_reqs):
        """
        Calculate soil suitability score (0-100)
        """
        score = 0

        # pH suitability (40% weight)
        ph_min, ph_max = crop_reqs["soil_pH_range"]
        if ph_min <= soil_ph <= ph_max:
            score += 40  # Perfect pH
        elif abs(soil_ph - ph_min) <= 0.5 or abs(soil_ph - ph_max) <= 0.5:
            score += 25  # Near optimal
        elif abs(soil_ph - ph_min) <= 1.0 or abs(soil_ph - ph_max) <= 1.0:
            score += 10  # Acceptable
        # Else: 0 points

        # Moisture suitability (30% weight)
        moisture_min, moisture_max = crop_reqs["moisture_range"]
        if moisture_min <= moisture <= moisture_max:
            score += 30  # Perfect moisture
        elif abs(moisture - moisture_min) <= 5 or abs(moisture - moisture_max) <= 5:
            score += 20  # Near optimal
        elif abs(moisture - moisture_min) <= 10 or abs(moisture - moisture_max) <= 10:
            score += 10  # Acceptable

        # pH and moisture compatibility bonus (10% weight)
        if ph_min <= soil_ph <= ph_max and moisture_min <= moisture <= moisture_max:
            score += 10

        return min(100, score)  # Cap at 100

    def calculate_nutrient_balance_score(self, n, p, k, crop_reqs):
        """
        Calculate nutrient balance score (0-100)
        """
        score = 0

        # Nitrogen (25% weight)
        n_min, n_max = crop_reqs["nitrogen_range"]
        if n_min <= n <= n_max:
            score += 25
        elif abs(n - n_min) <= 20 or abs(n - n_max) <= 20:
            score += 15
        elif abs(n - n_min) <= 40 or abs(n - n_max) <= 40:
            score += 5

        # Phosphorus (25% weight)
        p_min, p_max = crop_reqs["phosphorus_range"]
        if p_min <= p <= p_max:
            score += 25
        elif abs(p - p_min) <= 10 or abs(p - p_max) <= 10:
            score += 15
        elif abs(p - p_min) <= 20 or abs(p - p_max) <= 20:
            score += 5

        # Potassium (30% weight) - High weight due to importance
        k_min, k_max = crop_reqs["potassium_range"]
        if k_min <= k <= k_max:
            score += 30
        elif abs(k - k_min) <= 20 or abs(k - k_max) <= 20:
            score += 20
        elif abs(k - k_min) <= 40 or abs(k - k_max) <= 40:
            score += 10

        # Nutrient balance bonus (20% weight)
        nutrient_levels = [n, p, k]
        nutrient_reqs = [
            crop_reqs["nitrogen_range"],
            crop_reqs["phosphorus_range"],
            crop_reqs["potassium_range"]
        ]

        balance_score = 0
        for i, (level, req) in enumerate(zip(nutrient_levels, nutrient_reqs)):
            req_center = (req[0] + req[1]) / 2
            deviation = abs(level - req_center) / req_center
            balance_score += max(0, 1 - deviation)

        balance_score = (balance_score / 3) * 20  # Average and weight
        score += balance_score

        return min(100, score)

    def calculate_temperature_suitability_score(self, temperature, crop_reqs):
        """
        Calculate temperature suitability score (0-100)
        """
        temp_min, temp_max = crop_reqs["temperature_range"]
        optimal_temp = (temp_min + temp_max) / 2

        if temp_min <= temperature <= temp_max:
            # Within optimal range
            distance_from_optimal = abs(temperature - optimal_temp)
            max_distance = (temp_max - temp_min) / 2
            score = 100 * (1 - distance_from_optimal / max_distance)
            return max(10, score)  # Minimum 10 points
        else:
            # Outside optimal range
            deviation = min(abs(temperature - temp_min), abs(temperature - temp_max))
            if deviation <= 2:
                return 80
            elif deviation <= 5:
                return 60
            elif deviation <= 10:
                return 30
            else:
                return 10  # Very poor suitability

    def calculate_rainfall_suitability_score(self, rainfall, crop_reqs):
        """
        Calculate rainfall suitability score (0-100)
        """
        req_rainfall = crop_reqs.get("rainfall_requirement", 1000)

        if rainfall == req_rainfall:
            return 100  # Perfect match
        elif abs(rainfall - req_rainfall) <= 100:
            return 80  # Near optimal
        elif abs(rainfall - req_rainfall) <= 200:
            return 60  # Acceptable
        elif abs(rainfall - req_rainfall) <= 500:
            return 30  # Marginal
        else:
            return 10  # Poor suitability

    def calculate_district_agro_factor(self, district, crop_name):
        """
        Calculate district agro-zone suitability factor (0-100)
        """
        zone = get_district_zone(district)
        crop_reqs = get_crop_requirements(crop_name)

        if not crop_reqs:
            return 50  # Neutral score if crop not found

        zone_factor = crop_reqs["district_factor"].get(zone, 0.5)
        return zone_factor * 100  # Convert to 0-100 scale

    def calculate_overall_suitability_score(self, soil_data, district, temperature, crop_name):
        """
        Calculate overall suitability score using weighted components
        """
        crop_reqs = get_crop_requirements(crop_name)
        if not crop_reqs:
            return 0, "Crop requirements not available"

        # Component scores
        soil_score = self.calculate_soil_suitability_score(
            soil_data["pH"], soil_data["moisture"], crop_reqs
        )

        nutrient_score = self.calculate_nutrient_balance_score(
            soil_data["nitrogen"], soil_data["phosphorus"], soil_data["potassium"], crop_reqs
        )

        temp_score = self.calculate_temperature_suitability_score(temperature, crop_reqs)

        rainfall_score = self.calculate_rainfall_suitability_score(self.rainfall_mm, crop_reqs)

        district_score = self.calculate_district_agro_factor(district, crop_name)

        # Weighted overall score (out of 100)
        # Weights: Soil 20%, Nutrients 30%, Temperature 15%, Rainfall 20%, District 15%
        overall_score = (
            soil_score * 0.20 +
            nutrient_score * 0.30 +
            temp_score * 0.15 +
            rainfall_score * 0.20 +
            district_score * 0.15
        )

        return round(overall_score, 1)

    def generate_crop_reason(self, soil_data, district, temperature, crop_name, score):
        """
        Generate detailed reason for crop recommendation
        """
        crop_reqs = get_crop_requirements(crop_name)
        zone = get_district_zone(district)

        reasons = []

        # Soil pH assessment
        ph_min, ph_max = crop_reqs["soil_pH_range"]
        if ph_min <= soil_data["pH"] <= ph_max:
            reasons.append(f"Soil pH ({soil_data['pH']}) is optimal for {crop_name}")
        elif abs(soil_data["pH"] - ph_min) <= 0.5 or abs(soil_data["pH"] - ph_max) <= 0.5:
            reasons.append(f"Soil pH ({soil_data['pH']}) is near optimal for {crop_name}")

        # Nutrient assessment
        nutrients = {
            "Nitrogen": (soil_data["nitrogen"], crop_reqs["nitrogen_range"]),
            "Phosphorus": (soil_data["phosphorus"], crop_reqs["phosphorus_range"]),
            "Potassium": (soil_data["potassium"], crop_reqs["potassium_range"])
        }

        good_nutrients = []
        for nutrient, (level, req_range) in nutrients.items():
            if req_range[0] <= level <= req_range[1]:
                good_nutrients.append(nutrient)

        if good_nutrients:
            reasons.append(f"{' and '.join(good_nutrients)} levels are suitable for {crop_name}")

        # Temperature assessment
        temp_min, temp_max = crop_reqs["temperature_range"]
        if temp_min <= temperature <= temp_max:
            reasons.append(f"Temperature ({temperature}°C) is within optimal range for {crop_name}")

        # District suitability
        zone_factor = crop_reqs["district_factor"].get(zone, 0.5)
        if zone_factor >= 0.8:
            reasons.append(f"{crop_name} is well-suited for {zone} agro-climatic zone")
        elif zone_factor >= 0.6:
            reasons.append(f"{crop_name} is moderately suitable for {zone} agro-climatic zone")

        # Rainfall note
        reasons.append(f"Fixed rainfall of {self.rainfall_mm}mm is adequate for {crop_name}")

        return "; ".join(reasons)

    def recommend_crops(self, soil_ph, moisture_percentage, nitrogen, phosphorus,
                       potassium, temperature, district, top_n=3):
        """
        Main crop recommendation function
        """
        soil_data = {
            "pH": soil_ph,
            "moisture": moisture_percentage,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium
        }

        # Calculate scores for all crops
        crop_scores = []
        for crop in self.crops:
            score = self.calculate_overall_suitability_score(
                soil_data, district, temperature, crop
            )
            if score > 0:  # Only include crops with positive scores
                crop_scores.append((crop, score))

        # Sort by score (descending) and get top N
        crop_scores.sort(key=lambda x: x[1], reverse=True)
        top_crops = crop_scores[:top_n]

        # Generate recommendations
        recommendations = []
        for crop, score in top_crops:
            reason = self.generate_crop_reason(soil_data, district, temperature, crop, score)

            recommendation = {
                "crop": crop,
                "suitability_score": score,
                "reason": reason
            }
            recommendations.append(recommendation)

        # Get soil improvement suggestions for the top crop
        if recommendations:
            top_crop = recommendations[0]["crop"]
            crop_reqs = get_crop_requirements(top_crop)
            soil_improvements = get_complete_soil_improvement_plan(soil_data, crop_reqs, district)
        else:
            soil_improvements = {}

        return {
            "recommendations": recommendations,
            "soil_improvements": soil_improvements,
            "input_parameters": {
                "soil_pH": soil_ph,
                "moisture_percentage": moisture_percentage,
                "nitrogen_kgha": nitrogen,
                "phosphorus_kgha": phosphorus,
                "potassium_kgha": potassium,
                "temperature_celsius": temperature,
                "district": district,
                "rainfall_mm": self.rainfall_mm
            }
        }

    def recommend_crops_by_soil_conditions(self, soil_data, district=None, top_n=3):
        """
        Recommend crops using unified soil condition analyzer for consistency
        between sensor and satellite data sources

        Args:
            soil_data: Dictionary containing soil parameters (pH, moisture, N, P, K)
            district: District name for location-specific adjustments
            top_n: Number of top recommendations to return

        Returns:
            Dictionary with soil analysis and crop recommendations
        """
        # Use the unified soil condition analyzer
        analysis = soil_analyzer.analyze_soil_conditions(soil_data, district)

        # Limit to top_n recommendations
        recommendations = analysis['recommendations'][:top_n]

        # Add additional context from traditional recommender
        enhanced_recommendations = []
        for rec in recommendations:
            crop_name = rec['crop']
            crop_reqs = get_crop_requirements(crop_name)

            # Get soil improvement suggestions
            soil_improvements = get_complete_soil_improvement_plan(soil_data, crop_reqs, district or "")

            enhanced_rec = {
                "crop": crop_name,
                "suitability_score": rec['suitability_score'],
                "compatibility": rec['compatibility'],
                "reason": rec['reason'],
                "soil_improvements": soil_improvements
            }
            enhanced_recommendations.append(enhanced_rec)

        return {
            "recommendations": enhanced_recommendations,
            "soil_analysis": analysis['soil_analysis'],
            "zone": analysis['zone'],
            "district": analysis['district'],
            "input_parameters": soil_data
        }

    def recommend_crops_dynamically(self, latitude, longitude, sensor_id=None, data_source="satellite",
                                   district=None, top_n=3, previous_soil_data=None):
        """
        Dynamically recommend crops based on real-time satellite/sensor data and changing soil conditions.
        Adapts recommendations as soil conditions change over time.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            sensor_id: IoT sensor ID (optional, for sensor data)
            data_source: "satellite" or "sensor" - preferred data source
            district: District name (optional, will be inferred from coordinates if not provided)
            top_n: Number of top recommendations to return
            previous_soil_data: Previous soil data to detect changes (optional)

        Returns:
            Dictionary with dynamic recommendations, soil analysis, and change detection
        """
        # Fetch real-time data based on data source preference
        if data_source == "sensor" and sensor_id:
            # Get sensor data
            sensor_data = get_iot_sensor_data(sensor_id, hours=24)
            current_soil_data = {
                "pH": sensor_data['latest_reading']['ph'],
                "moisture": sensor_data['latest_reading']['moisture'],
                "nitrogen": sensor_data['latest_reading']['nitrogen'],
                "phosphorus": sensor_data['latest_reading']['phosphorus'],
                "potassium": sensor_data['latest_reading']['potassium']
            }
            temperature = sensor_data['latest_reading']['temperature']
            rainfall = sensor_data['latest_reading']['rainfall']
        else:
            # Get satellite data (default)
            satellite_soil = get_satellite_soil_data(latitude, longitude)
            satellite_weather = get_satellite_weather_data(latitude, longitude)
            current_soil_data = {
                "pH": satellite_soil['ph'],
                "moisture": 50.0,  # Satellite may not provide moisture, use default
                "nitrogen": satellite_soil['nitrogen'],
                "phosphorus": satellite_soil['phosphorus'],
                "potassium": satellite_soil['potassium']
            }
            temperature = satellite_weather['temperature']
            rainfall = satellite_weather['rainfall']

        # Detect changes in soil conditions
        soil_changes = self._detect_soil_changes(current_soil_data, previous_soil_data)

        # Adjust recommendations based on changing conditions
        adjusted_recommendations = self._adjust_recommendations_for_changes(
            current_soil_data, district, temperature, top_n, soil_changes
        )

        # Add context about data source and changes
        data_source_info = {
            "data_source": data_source,
            "sensor_id": sensor_id if data_source == "sensor" else None,
            "coordinates": {"lat": latitude, "lon": longitude},
            "timestamp": sensor_data['latest_reading']['timestamp'] if data_source == "sensor" else "satellite_real_time"
        }

        return {
            "recommendations": adjusted_recommendations,
            "soil_analysis": soil_analyzer.analyze_soil_conditions(current_soil_data, district),
            "soil_changes": soil_changes,
            "data_source_info": data_source_info,
            "current_soil_data": current_soil_data,
            "temperature": temperature,
            "rainfall": rainfall
        }

    def _detect_soil_changes(self, current_soil_data, previous_soil_data):
        """
        Detect significant changes in soil conditions over time.
        """
        if not previous_soil_data:
            return {"status": "no_previous_data", "changes": []}

        changes = []
        thresholds = {
            "pH": 0.5,  # pH change threshold
            "moisture": 10.0,  # Moisture percentage change threshold
            "nitrogen": 20.0,  # NPK change thresholds
            "phosphorus": 10.0,
            "potassium": 30.0
        }

        for param, threshold in thresholds.items():
            if param in current_soil_data and param in previous_soil_data:
                current_val = current_soil_data[param]
                previous_val = previous_soil_data[param]
                change = current_val - previous_val
                if abs(change) >= threshold:
                    direction = "increased" if change > 0 else "decreased"
                    changes.append({
                        "parameter": param,
                        "change": round(change, 2),
                        "direction": direction,
                        "significant": True
                    })

        return {
            "status": "changes_detected" if changes else "no_significant_changes",
            "changes": changes
        }

    def _adjust_recommendations_for_changes(self, soil_data, district, temperature, top_n, soil_changes):
        """
        Adjust crop recommendations based on detected soil changes.
        Different crops are recommended for different soil conditions (e.g., rice for high moisture, sugarcane for others).
        """
        # Get base recommendations
        base_result = self.recommend_crops_by_soil_conditions(soil_data, district, top_n)
        recommendations = base_result['recommendations']

        # Apply adjustments based on soil changes and current conditions
        adjusted_recommendations = []

        for rec in recommendations:
            crop_name = rec['crop']
            adjusted_score = rec['suitability_score']
            reasons = [rec['reason']]

            # Adjust based on current soil conditions
            if soil_data['moisture'] > 65:  # High moisture conditions
                if crop_name.lower() in ['rice', 'paddy']:
                    adjusted_score += 10  # Boost rice for high moisture
                    reasons.append("High moisture conditions favor rice cultivation")
                elif crop_name.lower() in ['sugarcane']:
                    adjusted_score -= 5  # Reduce sugarcane preference in very high moisture
                    reasons.append("Very high moisture may affect sugarcane growth")
            elif soil_data['moisture'] < 40:  # Low moisture conditions
                if crop_name.lower() in ['groundnut', 'barley', 'wheat']:
                    adjusted_score += 8  # Boost drought-tolerant crops
                    reasons.append("Low moisture conditions favor drought-tolerant crops")
                elif crop_name.lower() in ['rice']:
                    adjusted_score -= 10  # Reduce rice preference in low moisture
                    reasons.append("Low moisture conditions are not ideal for rice")

            # Adjust based on pH conditions
            if soil_data['pH'] > 7.5:  # Alkaline soil
                if crop_name.lower() in ['barley', 'wheat']:
                    adjusted_score += 5  # Barley prefers alkaline soil
                    reasons.append("Alkaline soil conditions favor barley")
            elif soil_data['pH'] < 6.0:  # Acidic soil
                if crop_name.lower() in ['rice', 'tea']:
                    adjusted_score += 5  # Rice tolerates acidic soil
                    reasons.append("Acidic soil conditions are suitable for rice")

            # Adjust based on nutrient levels
            if soil_data['nitrogen'] > 60:  # High nitrogen
                if crop_name.lower() in ['rice', 'wheat', 'maize']:
                    adjusted_score += 5  # High nitrogen crops
                    reasons.append("High nitrogen levels support high-yielding crops")
            elif soil_data['potassium'] > 200:  # High potassium
                if crop_name.lower() in ['sugarcane', 'banana', 'potato']:
                    adjusted_score += 5  # Potassium-loving crops
                    reasons.append("High potassium levels favor sugarcane and similar crops")

            # Apply changes based on detected soil changes
            if soil_changes['status'] == 'changes_detected':
                for change in soil_changes['changes']:
                    if change['parameter'] == 'moisture' and change['direction'] == 'increased':
                        if crop_name.lower() in ['rice', 'paddy']:
                            adjusted_score += 5
                            reasons.append("Increasing moisture trends favor rice")
                        elif crop_name.lower() in ['sugarcane']:
                            adjusted_score += 3
                            reasons.append("Moisture increase supports sugarcane growth")
                    elif change['parameter'] == 'moisture' and change['direction'] == 'decreased':
                        if crop_name.lower() in ['groundnut', 'barley']:
                            adjusted_score += 5
                            reasons.append("Decreasing moisture trends favor drought-tolerant crops")

            # Ensure score stays within bounds
            adjusted_score = max(0, min(100, adjusted_score))

            adjusted_rec = rec.copy()
            adjusted_rec['suitability_score'] = round(adjusted_score, 1)
            adjusted_rec['reason'] = "; ".join(reasons)
            adjusted_rec['adjustments_applied'] = True

            adjusted_recommendations.append(adjusted_rec)

        # Re-sort by adjusted scores
        adjusted_recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)

        return adjusted_recommendations[:top_n]

# Global recommender instance
recommender = CropRecommender()

def recommend_crop(soil_ph, moisture_percentage, nitrogen, phosphorus, potassium,
                  temperature, district, top_n=3):
    """
    Convenience function for crop recommendation
    """
    return recommender.recommend_crops(
        soil_ph, moisture_percentage, nitrogen, phosphorus, potassium,
        temperature, district, top_n
    )

def recommend_crop_by_soil_conditions(soil_data, district=None, top_n=3):
    """
    Convenience function for soil condition-based crop recommendation
    Ensures consistent recommendations between sensor and satellite data

    Args:
        soil_data: Dictionary with soil parameters (pH, moisture, nitrogen, phosphorus, potassium)
        district: District name (optional)
        top_n: Number of recommendations to return

    Returns:
        Dictionary with recommendations and soil analysis
    """
    return recommender.recommend_crops_by_soil_conditions(soil_data, district, top_n)

def recommend_crop_dynamically(latitude, longitude, sensor_id=None, data_source="satellite",
                              district=None, top_n=3, previous_soil_data=None):
    """
    Convenience function for dynamic crop recommendation based on real-time data.
    Adapts recommendations based on changing soil conditions from satellite or sensor data.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        sensor_id: IoT sensor ID (optional, for sensor data)
        data_source: "satellite" or "sensor" - preferred data source
        district: District name (optional)
        top_n: Number of recommendations to return
        previous_soil_data: Previous soil data to detect changes (optional)

    Returns:
        Dictionary with dynamic recommendations, soil analysis, and change detection
    """
    return recommender.recommend_crops_dynamically(
        latitude, longitude, sensor_id, data_source, district, top_n, previous_soil_data
    )

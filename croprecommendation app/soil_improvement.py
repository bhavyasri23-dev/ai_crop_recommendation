"""
Soil Improvement Recommendations Module
Provides suggestions for soil pH correction, fertilizer recommendations, and irrigation advice
"""

def get_ph_correction_recommendments(current_ph, target_ph_range):
    """
    Get recommendations for pH correction based on current and target pH
    """
    recommendations = []

    if current_ph < target_ph_range[0]:
        # Soil is too acidic, needs liming
        ph_difference = target_ph_range[0] - current_ph
        if ph_difference <= 0.5:
            recommendations.append("Apply 1-2 tons of lime per acre to raise soil pH")
        elif ph_difference <= 1.0:
            recommendations.append("Apply 2-3 tons of lime per acre to raise soil pH")
        else:
            recommendations.append("Apply 3-4 tons of lime per acre to raise soil pH")
        recommendations.append("Use dolomite lime if magnesium is also deficient")

    elif current_ph > target_ph_range[1]:
        # Soil is too alkaline, needs acidification
        ph_difference = current_ph - target_ph_range[1]
        if ph_difference <= 0.5:
            recommendations.append("Apply elemental sulfur (200-400 lbs/acre) to lower soil pH")
        else:
            recommendations.append("Apply elemental sulfur (400-600 lbs/acre) to lower soil pH")
        recommendations.append("Consider using acidifying fertilizers like ammonium sulfate")

    else:
        recommendations.append("Soil pH is within optimal range - no correction needed")

    return recommendations

def get_fertilizer_recommendations(nitrogen, phosphorus, potassium, crop_requirements):
    """
    Get fertilizer recommendations based on current nutrient levels and crop requirements
    """
    recommendations = []

    # Nitrogen recommendations
    n_deficit = crop_requirements["nitrogen_range"][0] - nitrogen
    if n_deficit > 20:
        recommendations.append(f"Apply {n_deficit:.0f} kg/ha additional nitrogen fertilizer")
        recommendations.append("Use urea or ammonium nitrate as nitrogen source")
    elif n_deficit > 0:
        recommendations.append(f"Apply {n_deficit:.0f} kg/ha nitrogen to meet crop requirements")

    # Phosphorus recommendations
    p_deficit = crop_requirements["phosphorus_range"][0] - phosphorus
    if p_deficit > 10:
        recommendations.append(f"Apply {p_deficit:.0f} kg/ha additional phosphorus fertilizer")
        recommendations.append("Use single superphosphate or diammonium phosphate")
    elif p_deficit > 0:
        recommendations.append(f"Apply {p_deficit:.0f} kg/ha phosphorus to meet crop requirements")

    # Potassium recommendations
    k_deficit = crop_requirements["potassium_range"][0] - potassium
    if k_deficit > 20:
        recommendations.append(f"Apply {k_deficit:.0f} kg/ha additional potassium fertilizer")
        recommendations.append("Use muriate of potash or potassium sulfate")
    elif k_deficit > 0:
        recommendations.append(f"Apply {k_deficit:.0f} kg/ha potassium to meet crop requirements")

    if not recommendations:
        recommendations.append("Nutrient levels are adequate for the recommended crop")

    return recommendations

def get_irrigation_recommendments(moisture_percentage, crop_requirements):
    """
    Get irrigation recommendations based on current moisture and crop requirements
    """
    recommendations = []

    moisture_deficit = crop_requirements["moisture_range"][0] - moisture_percentage

    if moisture_deficit > 20:
        recommendations.append("Immediate irrigation required - soil moisture is critically low")
        recommendations.append("Apply 50-70 mm of water per irrigation")
    elif moisture_deficit > 10:
        recommendations.append("Irrigation needed within 2-3 days")
        recommendations.append("Apply 40-50 mm of water per irrigation")
    elif moisture_deficit > 0:
        recommendations.append("Light irrigation may be beneficial")
        recommendations.append("Monitor soil moisture closely")

    if moisture_percentage > crop_requirements["moisture_range"][1]:
        recommendations.append("Reduce irrigation frequency - soil may be over-saturated")
        recommendations.append("Improve drainage to prevent waterlogging")

    # General irrigation advice
    recommendations.append("Use drip irrigation for water efficiency")
    recommendations.append("Irrigate early morning or evening to minimize evaporation")
    recommendations.append("Monitor soil moisture regularly with moisture meters")

    return recommendations

def get_organic_matter_recommendations():
    """
    General recommendations for improving soil organic matter
    """
    return [
        "Apply 5-10 tons of farmyard manure per acre annually",
        "Practice crop rotation to maintain soil fertility",
        "Include legumes in rotation for natural nitrogen fixation",
        "Use green manuring crops during fallow periods",
        "Avoid excessive tillage to preserve soil structure"
    ]

def get_complete_soil_improvement_plan(soil_data, crop_requirements, district):
    """
    Generate a complete soil improvement plan
    """
    plan = {
        "pH_correction": get_ph_correction_recommendments(
            soil_data["pH"], crop_requirements["soil_pH_range"]
        ),
        "fertilizer_recommendations": get_fertilizer_recommendations(
            soil_data["nitrogen"], soil_data["phosphorus"], soil_data["potassium"],
            crop_requirements
        ),
        "irrigation_advice": get_irrigation_recommendments(
            soil_data["moisture"], crop_requirements
        ),
        "organic_matter_improvement": get_organic_matter_recommendations(),
        "general_advice": [
            f"Recommendations tailored for {district} district conditions",
            "Test soil every 6-12 months to monitor changes",
            "Consult local agricultural extension services for specific advice",
            "Consider integrated nutrient management practices"
        ]
    }

    return plan

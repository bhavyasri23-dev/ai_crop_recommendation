"""
District Agro-Climatic Data for Andhra Pradesh
Contains agro-climatic zones and crop suitability data for each district
"""

# Andhra Pradesh Districts grouped by agro-climatic zones
AGRO_CLIMATIC_ZONES = {
    "Coastal Andhra": {
        "districts": ["Srikakulam", "Vizianagaram", "Visakhapatnam", "East Godavari", "West Godavari",
                     "Krishna", "Guntur", "Prakasam", "Nellore", "Chittoor"],
        "characteristics": {
            "soil_type": "coastal alluvial",
            "rainfall_range": "800-1200",
            "temperature_range": "24-32",
            "humidity": "high",
            "preferred_crops": ["Rice", "Sugarcane", "Coconut", "Banana", "Cashew"]
        }
    },
    "Rayalaseema": {
        "districts": ["Anantapur", "Kurnool", "Kadapa", "Chittoor"],
        "characteristics": {
            "soil_type": "red sandy loam",
            "rainfall_range": "500-800",
            "temperature_range": "28-35",
            "humidity": "medium",
            "preferred_crops": ["Groundnut", "Sunflower", "Cotton", "Chickpea", "Sorghum"]
        }
    },
    "North Coastal Andhra": {
        "districts": ["Srikakulam", "Vizianagaram", "Visakhapatnam"],
        "characteristics": {
            "soil_type": "lateritic",
            "rainfall_range": "1000-1400",
            "temperature_range": "25-30",
            "humidity": "high",
            "preferred_crops": ["Rice", "Cashew", "Banana", "Sugarcane", "Coconut"]
        }
    },
    "South Coastal Andhra": {
        "districts": ["East Godavari", "West Godavari", "Krishna", "Guntur", "Prakasam", "Nellore"],
        "characteristics": {
            "soil_type": "delta alluvial",
            "rainfall_range": "900-1300",
            "temperature_range": "26-32",
            "humidity": "high",
            "preferred_crops": ["Rice", "Sugarcane", "Cotton", "Banana", "Mango"]
        }
    }
}

# Crop database with suitability requirements
CROP_DATABASE = {
    "Rice": {
        "soil_pH_range": [5.5, 7.0],
        "moisture_range": [60, 80],
        "nitrogen_range": [80, 120],
        "phosphorus_range": [40, 60],
        "potassium_range": [40, 60],
        "temperature_range": [20, 35],
        "rainfall_requirement": 1000,
        "district_factor": {
            "Coastal Andhra": 1.0,
            "North Coastal Andhra": 0.9,
            "South Coastal Andhra": 0.95,
            "Rayalaseema": 0.6
        }
    },
    "Wheat": {
        "soil_pH_range": [6.0, 7.5],
        "moisture_range": [40, 60],
        "nitrogen_range": [100, 140],
        "phosphorus_range": [30, 50],
        "potassium_range": [30, 50],
        "temperature_range": [15, 25],
        "rainfall_requirement": 750,
        "district_factor": {
            "Coastal Andhra": 0.7,
            "North Coastal Andhra": 0.6,
            "South Coastal Andhra": 0.8,
            "Rayalaseema": 0.9
        }
    },
    "Cotton": {
        "soil_pH_range": [6.0, 8.0],
        "moisture_range": [30, 50],
        "nitrogen_range": [60, 100],
        "phosphorus_range": [20, 40],
        "potassium_range": [40, 60],
        "temperature_range": [25, 35],
        "rainfall_requirement": 600,
        "district_factor": {
            "Coastal Andhra": 0.8,
            "North Coastal Andhra": 0.7,
            "South Coastal Andhra": 0.9,
            "Rayalaseema": 1.0
        }
    },
    "Sugarcane": {
        "soil_pH_range": [6.5, 7.5],
        "moisture_range": [70, 90],
        "nitrogen_range": [150, 200],
        "phosphorus_range": [50, 80],
        "potassium_range": [100, 150],
        "temperature_range": [25, 35],
        "rainfall_requirement": 1500,
        "district_factor": {
            "Coastal Andhra": 1.0,
            "North Coastal Andhra": 0.9,
            "South Coastal Andhra": 1.0,
            "Rayalaseema": 0.7
        }
    },
    "Groundnut": {
        "soil_pH_range": [6.0, 7.5],
        "moisture_range": [30, 50],
        "nitrogen_range": [20, 40],
        "phosphorus_range": [30, 50],
        "potassium_range": [20, 40],
        "temperature_range": [25, 35],
        "rainfall_requirement": 500,
        "district_factor": {
            "Coastal Andhra": 0.8,
            "North Coastal Andhra": 0.7,
            "South Coastal Andhra": 0.9,
            "Rayalaseema": 1.0
        }
    },
    "Banana": {
        "soil_pH_range": [6.0, 7.5],
        "moisture_range": [60, 80],
        "nitrogen_range": [150, 200],
        "phosphorus_range": [40, 60],
        "potassium_range": [300, 400],  # High potassium requirement
        "temperature_range": [25, 35],
        "rainfall_requirement": 2000,
        "district_factor": {
            "Coastal Andhra": 1.0,
            "North Coastal Andhra": 1.0,
            "South Coastal Andhra": 0.9,
            "Rayalaseema": 0.8
        }
    },
    "Maize": {
        "soil_pH_range": [5.5, 7.0],
        "moisture_range": [50, 70],
        "nitrogen_range": [120, 160],
        "phosphorus_range": [40, 60],
        "potassium_range": [30, 50],
        "temperature_range": [20, 30],
        "rainfall_requirement": 600,
        "district_factor": {
            "Coastal Andhra": 0.9,
            "North Coastal Andhra": 0.8,
            "South Coastal Andhra": 1.0,
            "Rayalaseema": 0.9
        }
    },
    "Soybean": {
        "soil_pH_range": [6.0, 7.0],
        "moisture_range": [40, 60],
        "nitrogen_range": [20, 40],
        "phosphorus_range": [40, 60],
        "potassium_range": [20, 40],
        "temperature_range": [20, 30],
        "rainfall_requirement": 600,
        "district_factor": {
            "Coastal Andhra": 0.8,
            "North Coastal Andhra": 0.7,
            "South Coastal Andhra": 0.9,
            "Rayalaseema": 1.0
        }
    },
    "Chickpea": {
        "soil_pH_range": [6.0, 8.0],
        "moisture_range": [20, 40],
        "nitrogen_range": [20, 40],
        "phosphorus_range": [40, 60],
        "potassium_range": [20, 40],
        "temperature_range": [15, 25],
        "rainfall_requirement": 400,
        "district_factor": {
            "Coastal Andhra": 0.6,
            "North Coastal Andhra": 0.5,
            "South Coastal Andhra": 0.7,
            "Rayalaseema": 1.0
        }
    },
    "Sunflower": {
        "soil_pH_range": [6.0, 8.0],
        "moisture_range": [30, 50],
        "nitrogen_range": [50, 80],
        "phosphorus_range": [40, 60],
        "potassium_range": [30, 50],
        "temperature_range": [20, 30],
        "rainfall_requirement": 500,
        "district_factor": {
            "Coastal Andhra": 0.7,
            "North Coastal Andhra": 0.6,
            "South Coastal Andhra": 0.8,
            "Rayalaseema": 1.0
        }
    }
}

def get_district_zone(district):
    """
    Get the agro-climatic zone for a given district
    """
    for zone, data in AGRO_CLIMATIC_ZONES.items():
        if district in data["districts"]:
            return zone
    return "Coastal Andhra"  # Default fallback

def get_zone_characteristics(zone):
    """
    Get characteristics for a specific agro-climatic zone
    """
    return AGRO_CLIMATIC_ZONES.get(zone, AGRO_CLIMATIC_ZONES["Coastal Andhra"])

def get_crop_requirements(crop_name):
    """
    Get suitability requirements for a specific crop
    """
    return CROP_DATABASE.get(crop_name, {})

def get_all_crops():
    """
    Get list of all available crops
    """
    return list(CROP_DATABASE.keys())

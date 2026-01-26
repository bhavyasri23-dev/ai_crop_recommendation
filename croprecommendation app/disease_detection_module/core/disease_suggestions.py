"""
Disease Treatment Suggestions Module
Provides treatment recommendations and preventive measures for detected plant diseases
"""

from typing import Dict, List, Optional

class DiseaseSuggestions:
    """
    Provides treatment suggestions and preventive measures for plant diseases
    """

    def __init__(self):
        # Comprehensive disease treatment database
        self.disease_treatments = {
            "Corn Blight": {
                "immediate_actions": [
                    "Remove and destroy infected plant parts immediately",
                    "Apply copper-based fungicide (e.g., Bordeaux mixture)",
                    "Improve air circulation by proper plant spacing"
                ],
                "preventive_measures": [
                    "Use disease-resistant corn varieties",
                    "Rotate crops annually",
                    "Avoid overhead irrigation",
                    "Ensure proper field drainage"
                ],
                "chemical_treatments": [
                    "Azoxystrobin (e.g., Quadris)",
                    "Chlorothalonil (e.g., Bravo)",
                    "Mancozeb (e.g., Dithane)"
                ],
                "organic_alternatives": [
                    "Neem oil spray",
                    "Baking soda solution (1 tsp per quart water)",
                    "Compost tea applications"
                ]
            },
            "Corn Common Rust": {
                "immediate_actions": [
                    "Remove infected leaves and dispose of them",
                    "Apply fungicide at first sign of symptoms",
                    "Increase plant spacing for better air flow"
                ],
                "preventive_measures": [
                    "Plant rust-resistant varieties",
                    "Avoid working in wet fields",
                    "Ensure adequate plant nutrition",
                    "Practice crop rotation"
                ],
                "chemical_treatments": [
                    "Triazole fungicides (e.g., Tilt)",
                    "Strobilurin fungicides (e.g., Headline)",
                    "Chlorothalonil (e.g., Bravo)"
                ],
                "organic_alternatives": [
                    "Sulfur dust applications",
                    "Copper fungicide sprays",
                    "Beneficial bacteria (Bacillus subtilis)"
                ]
            },
            "Corn Gray Leaf Spot": {
                "immediate_actions": [
                    "Remove infected leaves from lower plant parts",
                    "Apply fungicide when lesions first appear",
                    "Ensure proper nitrogen fertilization"
                ],
                "preventive_measures": [
                    "Use resistant hybrid varieties",
                    "Practice tillage to bury crop residues",
                    "Avoid late planting",
                    "Maintain proper plant population"
                ],
                "chemical_treatments": [
                    "Strobilurin fungicides (e.g., Headline)",
                    "Triazole fungicides (e.g., Proline)",
                    "Chlorothalonil (e.g., Bravo)"
                ],
                "organic_alternatives": [
                    "Neem oil applications",
                    "Compost extracts",
                    "Silicon supplements for plant strength"
                ]
            },
            "Rice Bacterial Blight": {
                "immediate_actions": [
                    "Remove infected plants immediately",
                    "Apply copper-based bactericide",
                    "Avoid working in wet fields"
                ],
                "preventive_measures": [
                    "Use resistant rice varieties",
                    "Avoid excessive nitrogen fertilization",
                    "Practice proper water management",
                    "Implement seed treatment"
                ],
                "chemical_treatments": [
                    "Copper hydroxide (e.g., Kocide)",
                    "Streptomycin (for seed treatment)",
                    "Oxytetracycline (limited use)"
                ],
                "organic_alternatives": [
                    "Garlic extract sprays",
                    "Chili extract solutions",
                    "Bio-control agents (Pseudomonas fluorescens)"
                ]
            },
            "Rice Brown Spot": {
                "immediate_actions": [
                    "Apply fungicide at tillering stage",
                    "Improve field drainage",
                    "Reduce nitrogen application if excessive"
                ],
                "preventive_measures": [
                    "Use balanced fertilization",
                    "Avoid drought stress",
                    "Practice proper water management",
                    "Use certified disease-free seeds"
                ],
                "chemical_treatments": [
                    "Mancozeb (e.g., Dithane)",
                    "Carbendazim (e.g., Bavistin)",
                    "Tricyclazole (e.g., Beam)"
                ],
                "organic_alternatives": [
                    "Neem cake application",
                    "Trichoderma viride treatment",
                    "Silicon fertilization"
                ]
            },
            "Rice Leaf Blast": {
                "immediate_actions": [
                    "Apply systemic fungicide immediately",
                    "Remove infected leaves",
                    "Reduce nitrogen fertilization"
                ],
                "preventive_measures": [
                    "Use blast-resistant varieties",
                    "Avoid excessive nitrogen",
                    "Practice proper plant spacing",
                    "Implement field sanitation"
                ],
                "chemical_treatments": [
                    "Tricyclazole (e.g., Beam)",
                    "Isoprothiolane (e.g., Fuji-One)",
                    "Carbendazim (e.g., Bavistin)"
                ],
                "organic_alternatives": [
                    "Silicon applications",
                    "Potassium bicarbonate sprays",
                    "Bio-control agents"
                ]
            },
            "Wheat Black Chaff": {
                "immediate_actions": [
                    "Apply fungicide at heading stage",
                    "Ensure proper plant nutrition",
                    "Improve air circulation"
                ],
                "preventive_measures": [
                    "Use resistant wheat varieties",
                    "Practice crop rotation",
                    "Avoid late sowing",
                    "Maintain proper plant density"
                ],
                "chemical_treatments": [
                    "Tebuconazole (e.g., Folicur)",
                    "Propiconazole (e.g., Tilt)",
                    "Azoxystrobin (e.g., Amistar)"
                ],
                "organic_alternatives": [
                    "Copper fungicides",
                    "Sulfur applications",
                    "Compost tea sprays"
                ]
            },
            "Wheat Leaf Rust": {
                "immediate_actions": [
                    "Apply fungicide at first rust pustules",
                    "Remove volunteer wheat plants",
                    "Improve field drainage"
                ],
                "preventive_measures": [
                    "Plant rust-resistant varieties",
                    "Practice crop rotation",
                    "Avoid late planting",
                    "Ensure balanced fertilization"
                ],
                "chemical_treatments": [
                    "Triazole fungicides (e.g., Tilt)",
                    "Strobilurin fungicides (e.g., Headline)",
                    "Mancozeb (e.g., Dithane)"
                ],
                "organic_alternatives": [
                    "Sulfur dust",
                    "Neem oil sprays",
                    "Bio-control fungi (Trichoderma)"
                ]
            },
            "Wheat Powdery Mildew": {
                "immediate_actions": [
                    "Apply fungicide when mildew first appears",
                    "Improve air circulation",
                    "Reduce plant density if needed"
                ],
                "preventive_measures": [
                    "Use mildew-resistant varieties",
                    "Avoid excessive nitrogen",
                    "Ensure proper plant spacing",
                    "Practice field sanitation"
                ],
                "chemical_treatments": [
                    "Tebuconazole (e.g., Folicur)",
                    "Myclobutanil (e.g., Systhane)",
                    "Sulfur-based fungicides"
                ],
                "organic_alternatives": [
                    "Baking soda sprays",
                    "Milk solution (1:9 ratio)",
                    "Neem oil applications"
                ]
            },
            "Tomato Bacterial Spot": {
                "immediate_actions": [
                    "Remove infected plants and destroy them",
                    "Apply copper bactericide",
                    "Disinfect tools between plants"
                ],
                "preventive_measures": [
                    "Use disease-resistant varieties",
                    "Avoid overhead irrigation",
                    "Practice crop rotation",
                    "Implement proper sanitation"
                ],
                "chemical_treatments": [
                    "Copper hydroxide (e.g., Kocide)",
                    "Mancozeb (e.g., Dithane)",
                    "Chlorothalonil (e.g., Bravo)"
                ],
                "organic_alternatives": [
                    "Garlic extract sprays",
                    "Chili pepper extracts",
                    "Bio-control bacteria"
                ]
            },
            "Tomato Early Blight": {
                "immediate_actions": [
                    "Remove infected leaves",
                    "Apply fungicide immediately",
                    "Mulch around plants to prevent soil splash"
                ],
                "preventive_measures": [
                    "Use resistant varieties",
                    "Practice crop rotation",
                    "Avoid overhead watering",
                    "Ensure proper plant spacing"
                ],
                "chemical_treatments": [
                    "Chlorothalonil (e.g., Bravo)",
                    "Mancozeb (e.g., Dithane)",
                    "Copper fungicides"
                ],
                "organic_alternatives": [
                    "Neem oil sprays",
                    "Baking soda solutions",
                    "Compost tea applications"
                ]
            },
            "Tomato Late Blight": {
                "immediate_actions": [
                    "Remove all infected plant material",
                    "Apply systemic fungicide immediately",
                    "Destroy infected plants completely"
                ],
                "preventive_measures": [
                    "Use late blight-resistant varieties",
                    "Avoid overhead irrigation",
                    "Improve air circulation",
                    "Practice crop rotation"
                ],
                "chemical_treatments": [
                    "Mancozeb (e.g., Dithane)",
                    "Chlorothalonil (e.g., Bravo)",
                    "Metalaxyl (e.g., Ridomil)"
                ],
                "organic_alternatives": [
                    "Copper fungicides",
                    "Bio-control agents",
                    "Plant extracts (garlic, neem)"
                ]
            },
            "Cucumber Downy Mildew": {
                "immediate_actions": [
                    "Apply fungicide at first symptoms",
                    "Remove infected leaves",
                    "Improve air circulation"
                ],
                "preventive_measures": [
                    "Use resistant varieties",
                    "Avoid overhead watering",
                    "Ensure proper plant spacing",
                    "Practice crop rotation"
                ],
                "chemical_treatments": [
                    "Mancozeb (e.g., Dithane)",
                    "Chlorothalonil (e.g., Bravo)",
                    "Cymoxanil (e.g., Curzate)"
                ],
                "organic_alternatives": [
                    "Neem oil sprays",
                    "Baking soda solutions",
                    "Milk sprays (1:9 ratio)"
                ]
            },
            "Cucumber Powdery Mildew": {
                "immediate_actions": [
                    "Apply fungicide when mildew appears",
                    "Remove severely infected leaves",
                    "Improve air circulation"
                ],
                "preventive_measures": [
                    "Use mildew-resistant varieties",
                    "Avoid excessive nitrogen",
                    "Ensure proper plant spacing",
                    "Practice field sanitation"
                ],
                "chemical_treatments": [
                    "Myclobutanil (e.g., Systhane)",
                    "Tebuconazole (e.g., Folicur)",
                    "Sulfur-based fungicides"
                ],
                "organic_alternatives": [
                    "Baking soda sprays",
                    "Milk solution applications",
                    "Neem oil treatments"
                ]
            },
            "Potato Early Blight": {
                "immediate_actions": [
                    "Remove infected leaves",
                    "Apply fungicide immediately",
                    "Avoid working in wet conditions"
                ],
                "preventive_measures": [
                    "Use resistant varieties",
                    "Practice crop rotation",
                    "Avoid overhead irrigation",
                    "Ensure proper hilling"
                ],
                "chemical_treatments": [
                    "Chlorothalonil (e.g., Bravo)",
                    "Mancozeb (e.g., Dithane)",
                    "Copper fungicides"
                ],
                "organic_alternatives": [
                    "Neem oil sprays",
                    "Compost tea applications",
                    "Bio-control agents"
                ]
            },
            "Potato Late Blight": {
                "immediate_actions": [
                    "Destroy all infected plants immediately",
                    "Apply fungicide urgently",
                    "Avoid handling wet plants"
                ],
                "preventive_measures": [
                    "Use late blight-resistant varieties",
                    "Avoid overhead irrigation",
                    "Improve field drainage",
                    "Practice long crop rotations"
                ],
                "chemical_treatments": [
                    "Mancozeb (e.g., Dithane)",
                    "Chlorothalonil (e.g., Bravo)",
                    "Metalaxyl (e.g., Ridomil)"
                ],
                "organic_alternatives": [
                    "Copper fungicides",
                    "Bio-control bacteria",
                    "Plant extract sprays"
                ]
            },
            "Soybean Bacterial Blight": {
                "immediate_actions": [
                    "Apply copper bactericide",
                    "Remove infected leaves",
                    "Improve field drainage"
                ],
                "preventive_measures": [
                    "Use resistant varieties",
                    "Practice crop rotation",
                    "Avoid working in wet fields",
                    "Implement seed treatment"
                ],
                "chemical_treatments": [
                    "Copper hydroxide (e.g., Kocide)",
                    "Mancozeb (e.g., Dithane)",
                    "Streptomycin (seed treatment)"
                ],
                "organic_alternatives": [
                    "Garlic extract sprays",
                    "Bio-control agents",
                    "Copper sulfate solutions"
                ]
            },
            "Soybean Frogeye Leaf Spot": {
                "immediate_actions": [
                    "Apply fungicide at first spots",
                    "Remove infected leaves",
                    "Ensure balanced fertilization"
                ],
                "preventive_measures": [
                    "Use resistant varieties",
                    "Practice crop rotation",
                    "Avoid excessive nitrogen",
                    "Maintain proper plant spacing"
                ],
                "chemical_treatments": [
                    "Azoxystrobin (e.g., Quadris)",
                    "Tebuconazole (e.g., Folicur)",
                    "Chlorothalonil (e.g., Bravo)"
                ],
                "organic_alternatives": [
                    "Neem oil applications",
                    "Copper fungicides",
                    "Bio-control fungi"
                ]
            }
        }

        # General healthy plant advice
        self.healthy_advice = {
            "maintenance": [
                "Continue regular monitoring for early disease detection",
                "Maintain proper irrigation and fertilization schedule",
                "Ensure good air circulation around plants",
                "Practice proper weed management"
            ],
            "prevention": [
                "Keep fields clean of plant debris",
                "Monitor for pest and disease regularly",
                "Maintain proper plant nutrition",
                "Use certified disease-free seeds"
            ]
        }

    def get_suggestions(self, disease_name: str, preference: str = "balanced") -> Dict:
        """
        Get treatment suggestions for a specific disease
        preference: "chemical", "organic", or "balanced"
        """
        # Normalize disease name
        normalized_name = self._normalize_disease_name(disease_name)

        if normalized_name not in self.disease_treatments:
            return {
                "error": f"No suggestions available for {disease_name}",
                "general_advice": [
                    "Consult local agricultural extension service",
                    "Monitor plant health regularly",
                    "Maintain proper cultural practices",
                    "Consider professional diagnosis"
                ]
            }

        treatment_info = self.disease_treatments[normalized_name]

        suggestions = {
            "disease": normalized_name,
            "immediate_actions": treatment_info["immediate_actions"],
            "preventive_measures": treatment_info["preventive_measures"]
        }

        # Add treatment options based on preference
        if preference == "chemical":
            suggestions["recommended_treatments"] = treatment_info["chemical_treatments"]
        elif preference == "organic":
            suggestions["recommended_treatments"] = treatment_info["organic_alternatives"]
        else:  # balanced
            suggestions["chemical_options"] = treatment_info["chemical_treatments"]
            suggestions["organic_options"] = treatment_info["organic_alternatives"]

        return suggestions

    def get_healthy_suggestions(self) -> Dict:
        """Get suggestions for healthy plants"""
        return {
            "status": "healthy",
            "maintenance_tips": self.healthy_advice["maintenance"],
            "prevention_tips": self.healthy_advice["prevention"],
            "monitoring_advice": [
                "Continue regular field inspections",
                "Watch for early signs of stress or disease",
                "Maintain records of plant health",
                "Prepare for seasonal disease pressures"
            ]
        }

    def _normalize_disease_name(self, disease_name: str) -> str:
        """Normalize disease name to match database keys"""
        # Handle various formats
        name = disease_name.strip()

        # Convert to title case and handle special cases
        if name.lower() == "healthy":
            return "Healthy"

        # Remove extra spaces and standardize
        name = ' '.join(name.split())

        # Map common variations to standard names
        name_mapping = {
            "corn blight": "Corn Blight",
            "corn common rust": "Corn Common Rust",
            "corn gray leaf spot": "Corn Gray Leaf Spot",
            "rice bacterial blight": "Rice Bacterial Blight",
            "rice brown spot": "Rice Brown Spot",
            "rice leaf blast": "Rice Leaf Blast",
            "wheat black chaff": "Wheat Black Chaff",
            "wheat leaf rust": "Wheat Leaf Rust",
            "wheat powdery mildew": "Wheat Powdery Mildew",
            "tomato bacterial spot": "Tomato Bacterial Spot",
            "tomato early blight": "Tomato Early Blight",
            "tomato late blight": "Tomato Late Blight",
            "cucumber downy mildew": "Cucumber Downy Mildew",
            "cucumber powdery mildew": "Cucumber Powdery Mildew",
            "potato early blight": "Potato Early Blight",
            "potato late blight": "Potato Late Blight",
            "soybean bacterial blight": "Soybean Bacterial Blight",
            "soybean frogeye leaf spot": "Soybean Frogeye Leaf Spot"
        }

        return name_mapping.get(name.lower(), name)

    def get_all_supported_diseases(self) -> List[str]:
        """Get list of all diseases with available suggestions"""
        return list(self.disease_treatments.keys())

# Global instance
disease_suggestions = DiseaseSuggestions()

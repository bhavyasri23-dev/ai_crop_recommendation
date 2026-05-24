"""
Example usage of Grove AI Plant Disease Detection Module

This script demonstrates how to use the Grove AI module for plant disease detection.
"""

import sys
import os

# Add the parent directory to Python path to import grove_ai
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grove_ai import GroveAI

def main():
    """
    Example usage of Grove AI module.
    """
    print("Grove AI - Plant Disease Detection Example")
    print("=" * 50)

    # Initialize Grove AI
    print("Initializing Grove AI...")
    detector = GroveAI(confidence_threshold=0.7)

    # Display supported plants
    supported_plants = detector.get_supported_plants()
    print(f"Supported plants: {', '.join(supported_plants)}")

    # Example 1: Check supported diseases for tomato
    print("\nExample 1: Supported diseases for tomato")
    tomato_diseases = detector.get_supported_diseases('tomato')
    if tomato_diseases:
        print(f"Tomato diseases: {', '.join(tomato_diseases)}")
    else:
        print("No diseases found for tomato")

    # Example 2: Simulate analysis with dummy data
    print("\nExample 2: Simulated plant analysis")
    print("Note: This is a simulation since we don't have actual image data")

    # In a real scenario, you would load image bytes like this:
    # with open('plant_leaf.jpg', 'rb') as f:
    #     image_data = f.read()
    # result = detector.analyze_plant(image_data)

    # For demonstration, we'll show the expected result structure
    print("Expected result structure:")
    print("""
    {
        'success': True,
        'plant_type': 'tomato',
        'plant_confidence': 0.85,
        'disease': 'healthy',
        'disease_confidence': 0.92,
        'recommendations': {
            'cause': 'No disease detected',
            'treatment': 'Continue regular care and monitoring',
            'prevention': 'Maintain proper watering, fertilization, and pest monitoring'
        }
    }
    """)

    # Example 3: Error handling
    print("Example 3: Error handling for unsupported plant")
    try:
        diseases = detector.get_supported_diseases('apple')
        if diseases is None:
            print("Apple is not a supported plant type")
    except Exception as e:
        print(f"Error: {e}")

    # Cleanup
    print("\nCleaning up resources...")
    detector.cleanup()

    print("Example completed successfully!")

if __name__ == "__main__":
    main()

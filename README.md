Modular AI Agricultural Assistant
A production-ready, modular AI system providing deterministic agricultural decision support through two independent modules with strict single-output guarantees.

🏗️ Architecture
This system has been refactored from a monolithic application into two strict and independent modules:

🌾 Crop Recommendation Module (Port 5001)

Purpose: Deterministic crop recommendations based on soil conditions

Input: District + soil parameters (pH, N, P, rainfall)

Output: Exactly 1 crop recommendation (no ambiguity, no multiple suggestions)

Technology: Flask + Deterministic Rules Engine

Validation: Cross-validates manual, satellite, and IoT sensor data

🔍 Disease Detection Module (Port 5002)

Purpose: Single-output plant disease identification

Input: Plant image + optional crop type

Output: Exactly 1 result ("Healthy" or specific disease name)

Technology: Flask + TensorFlow CNN

Validation: Image quality assessment and leaf detection

#!/usr/bin/env python3
"""
Launcher script to run both crop recommendation and disease detection modules
Crop Recommendation: http://localhost:5002
Disease Detection: http://localhost:5001
"""

import subprocess
import sys
import os
import time
import threading

def run_crop_module():
    """Run the crop recommendation module on port 5002"""
    print("🚀 Starting Crop Recommendation Module on port 5002...")
    os.chdir('crop_recommendation_module')
    subprocess.run([sys.executable, 'app.py'])

def run_disease_module():
    """Run the disease detection module on port 5001"""
    print("🔬 Starting Disease Detection Module on port 5001...")
    time.sleep(2)  # Small delay to let crop module start first
    os.chdir('disease_detection_module')
    subprocess.run([sys.executable, 'app.py'])

if __name__ == '__main__':
    print("🌾 Starting AI Crop Recommendation System")
    print("==========================================")
    print("Crop Recommendation Module: http://localhost:5002")
    print("Disease Detection Module: http://localhost:5001")
    print("Press Ctrl+C to stop both modules")
    print("==========================================")

    # Start both modules in separate threads
    crop_thread = threading.Thread(target=run_crop_module)
    disease_thread = threading.Thread(target=run_disease_module)

    try:
        crop_thread.start()
        disease_thread.start()

        # Wait for both threads
        crop_thread.join()
        disease_thread.join()

    except KeyboardInterrupt:
        print("\n🛑 Stopping modules...")
        sys.exit(0)

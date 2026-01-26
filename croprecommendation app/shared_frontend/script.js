const CROP_API_BASE_URL = "http://localhost:5002";
const DISEASE_API_BASE_URL = "http://localhost:5003";

// IoT Status Indicator Functions
function showIoTStatus(message, icon) {
    const statusDiv = document.getElementById('iot-status');
    const statusIcon = document.getElementById('status-icon');
    const statusText = document.getElementById('status-text');

    if (statusDiv && statusIcon && statusText) {
        statusIcon.textContent = icon;
        statusText.textContent = message;
        statusDiv.style.display = 'block';
    }
}

function hideIoTStatus() {
    const statusDiv = document.getElementById('iot-status');
    if (statusDiv) {
        statusDiv.style.display = 'none';
    }
}

// Navigation functions

function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('main section');
    sections.forEach(section => section.classList.remove('active-section'));

    // Remove active class from nav buttons
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => btn.classList.remove('active'));

    // Show selected section
    const targetSection = document.getElementById(sectionName + '-prediction') || document.getElementById(sectionName);
    if (targetSection) {
        targetSection.classList.add('active-section');
    }

    // Add active class to clicked nav button
    const activeButton = document.querySelector(`[data-section="${sectionName}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

function setInputMethod(method) {
    // Hide all input sections
    const inputSections = document.querySelectorAll('.input-section');
    inputSections.forEach(section => section.classList.remove('active'));

    // Remove active class from method buttons
    const methodButtons = document.querySelectorAll('.method-btn');
    methodButtons.forEach(btn => btn.classList.remove('active'));

    // Show selected input section
    const targetInput = document.getElementById(method + '-inputs');
    if (targetInput) {
        targetInput.classList.add('active');
    }

    // Add active class to clicked method button
    const activeButton = document.querySelector(`[data-method="${method}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }

    // Auto-populate IoT sensor data when switching to IoT method
    if (method === 'iot') {
        const connectedSensor = localStorage.getItem('connectedSensor');
        if (connectedSensor) {
            document.getElementById('sensor-id').value = connectedSensor;
            populateFromIoTSensor();
        }
    }
}

function showTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));

    // Remove active class from tab buttons
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab content
    const targetTab = document.getElementById(tabName + '-tab');
    if (targetTab) {
        targetTab.classList.add('active');
    }

    // Add active class to clicked tab button
    const activeButton = document.querySelector(`.tab-btn[onclick="showTab('${tabName}')"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

// District soil data for satellite/IoT simulation
const DISTRICT_SOIL_DATA = {
    'vizianagaram': { ph: 6.6, nitrogen: 68, phosphorus: 195, potassium: 48, temperature: 27, humidity: 80, rainfall: 980 },
    'srikakulam': { ph: 6.2, nitrogen: 45, phosphorus: 180, potassium: 35, temperature: 28, humidity: 75, rainfall: 1100 },
    'east godavari': { ph: 6.8, nitrogen: 72, phosphorus: 200, potassium: 52, temperature: 29, humidity: 85, rainfall: 950 },
    'west godavari': { ph: 7.0, nitrogen: 65, phosphorus: 190, potassium: 50, temperature: 28, humidity: 82, rainfall: 1050 },
    'krishna': { ph: 7.2, nitrogen: 58, phosphorus: 175, potassium: 45, temperature: 30, humidity: 78, rainfall: 920 },
    'guntur': { ph: 7.5, nitrogen: 55, phosphorus: 165, potassium: 42, temperature: 31, humidity: 75, rainfall: 850 },
    'prakasam': { ph: 7.3, nitrogen: 52, phosphorus: 160, potassium: 40, temperature: 32, humidity: 72, rainfall: 780 },
    'nellore': { ph: 7.8, nitrogen: 48, phosphorus: 155, potassium: 38, temperature: 31, humidity: 70, rainfall: 780 },
    'kadapa': { ph: 7.6, nitrogen: 42, phosphorus: 140, potassium: 35, temperature: 33, humidity: 65, rainfall: 600 },
    'anantapur': { ph: 8.0, nitrogen: 38, phosphorus: 135, potassium: 32, temperature: 34, humidity: 60, rainfall: 520 },
    'kurnool': { ph: 8.2, nitrogen: 35, phosphorus: 130, potassium: 30, temperature: 35, humidity: 58, rainfall: 450 },
    'chittoor': { ph: 7.4, nitrogen: 40, phosphorus: 145, potassium: 36, temperature: 32, humidity: 68, rainfall: 700 }
};

async function fetchSatelliteData() {
    const currentDistrict = document.getElementById("location").value.trim();

    if (!currentDistrict) {
        alert('Please fill the district field first before using satellite data.');
        return;
    }

    const district = currentDistrict;

    // Get soil data for district
    const soilData = DISTRICT_SOIL_DATA[district.toLowerCase()];
    if (!soilData) {
        alert(`District ${district} not supported for satellite data. Please use manual input.`);
        return;
    }

    // Populate form with satellite data
    document.getElementById("ph").value = soilData.ph;
    document.getElementById("n").value = soilData.nitrogen;
    document.getElementById("p").value = soilData.phosphorus;
    document.getElementById("k").value = soilData.potassium;
    document.getElementById("temp").value = soilData.temperature;
    document.getElementById("moisture").value = soilData.humidity;
    document.getElementById("rainfall").value = soilData.rainfall;
    document.getElementById("location").value = district;

    // Fetch crop recommendation based on the district's soil data
    try {
        const payload = {
            district: district,
            nitrogen: soilData.nitrogen,
            phosphorus: soilData.phosphorus,
            pH: soilData.ph,
            rainfall: soilData.rainfall
        };

        const res = await fetch(`${CROP_API_BASE_URL}/api/recommend_crop`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            const response = await res.json();
            const result = response.data[0];
            alert(`Satellite data loaded!\n\nSoil Conditions:\n• pH: ${soilData.ph}\n• Nitrogen (N): ${soilData.nitrogen} kg/ha\n• Phosphorus (P): ${soilData.phosphorus} kg/ha\n• Potassium (K): ${soilData.potassium} kg/ha\n• Temperature: ${soilData.temperature}°C\n• Humidity: ${soilData.humidity}%\n• Rainfall: ${soilData.rainfall} mm/year\n\nRecommended Crop: ${result.recommendation}`);
        } else {
            alert(`Satellite data loaded!\n\nSoil Conditions:\n• pH: ${soilData.ph}\n• Nitrogen (N): ${soilData.nitrogen} kg/ha\n• Phosphorus (P): ${soilData.phosphorus} kg/ha\n• Potassium (K): ${soilData.potassium} kg/ha\n• Temperature: ${soilData.temperature}°C\n• Humidity: ${soilData.humidity}%\n• Rainfall: ${soilData.rainfall} mm/year\n\nClick "Get AI Recommendation" to see crop suggestions.`);
        }
    } catch (err) {
        alert(`Satellite data loaded!\n\nSoil Conditions:\n• pH: ${soilData.ph}\n• Nitrogen (N): ${soilData.nitrogen} kg/ha\n• Phosphorus (P): ${soilData.phosphorus} kg/ha\n• Potassium (K): ${soilData.potassium} kg/ha\n• Temperature: ${soilData.temperature}°C\n• Humidity: ${soilData.humidity}%\n• Rainfall: ${soilData.rainfall} mm/year\n\nClick "Get AI Recommendation" to see crop suggestions.`);
    }
}

function connectIoT() {
    const sensorId = document.getElementById("sensor-id").value.trim();
    if (!sensorId) {
        alert('Please enter a sensor ID');
        return;
    }

    // Simulate IoT connection
    localStorage.setItem('connectedSensor', sensorId);
    alert(`IoT Sensor ${sensorId} connected successfully!`);
}

async function populateFromIoTSensor() {
    const sensorId = localStorage.getItem('connectedSensor');
    if (!sensorId) {
        alert('No IoT sensor connected. Please connect a sensor first.');
        return;
    }

    showIoTStatus('Fetching real-time IoT sensor data...', '🔄');

    try {
        // Call the backend IoT integration API
        const iotResponse = await fetch(`${CROP_API_BASE_URL}/api/iot/sensor_data?sensor_id=${sensorId}&hours=24`);
        if (!iotResponse.ok) {
            throw new Error('Failed to fetch IoT sensor data');
        }

        const iotData = await iotResponse.json();
        const latestReading = iotData.latest_reading;

        showIoTStatus('Populating form with IoT data...', '📊');

        // Populate form with real IoT sensor data
        document.getElementById("ph").value = latestReading.ph;
        document.getElementById("n").value = latestReading.nitrogen;
        document.getElementById("p").value = latestReading.phosphorus;
        document.getElementById("k").value = latestReading.potassium;
        document.getElementById("temp").value = latestReading.temperature;
        document.getElementById("moisture").value = latestReading.moisture;
        document.getElementById("rainfall").value = latestReading.rainfall;

        // Extract district from sensor ID (ASU-AP-XX-DistrictName format)
        const districtMatch = sensorId.match(/ASU-AP-\d+-(.+)/);
        const district = districtMatch ? districtMatch[1] : sensorId;
        document.getElementById("location").value = district;

        showIoTStatus('Getting AI crop recommendation...', '🤖');

        // Get crop recommendation using the IoT data
        const payload = {
            sensor_id: sensorId
        };

        const res = await fetch(`${CROP_API_BASE_URL}/api/recommend_crop`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            const response = await res.json();
            const result = response.data[0];
            showIoTStatus('IoT Data Loaded Successfully!', '✅');
            setTimeout(() => hideIoTStatus(), 3000);
            alert(`IoT Sensor Data Loaded Successfully!\n\nReal-time Soil Conditions from ${sensorId}:\n• pH: ${latestReading.ph}\n• Nitrogen (N): ${latestReading.nitrogen} kg/ha\n• Phosphorus (P): ${latestReading.phosphorus} kg/ha\n• Potassium (K): ${latestReading.potassium} kg/ha\n• Temperature: ${latestReading.temperature}°C\n• Moisture: ${latestReading.moisture}%\n• Rainfall: ${latestReading.rainfall} mm\n\nAI Recommended Crop: ${result.recommendation} (${result.accuracy} accuracy)`);
        } else {
            showIoTStatus('IoT Data Loaded (Manual recommendation needed)', '⚠️');
            setTimeout(() => hideIoTStatus(), 3000);
            alert(`IoT Sensor Data Loaded!\n\nReal-time Soil Conditions from ${sensorId}:\n• pH: ${latestReading.ph}\n• Nitrogen (N): ${latestReading.nitrogen} kg/ha\n• Phosphorus (P): ${latestReading.phosphorus} kg/ha\n• Potassium (K): ${latestReading.potassium} kg/ha\n• Temperature: ${latestReading.temperature}°C\n• Moisture: ${latestReading.moisture}%\n• Rainfall: ${latestReading.rainfall} mm\n\nClick "Get AI Recommendation" to see crop suggestions.`);
        }

    } catch (err) {
        console.error('IoT sensor data fetch error:', err);
        showIoTStatus('Using simulated data (Backend unavailable)', '⚠️');
        setTimeout(() => hideIoTStatus(), 3000);
        alert(`Failed to load IoT sensor data: ${err.message}\n\nFalling back to simulated data for demonstration.`);

        // Fallback to simulated data if backend is not available
        const currentDistrict = document.getElementById("location").value.trim();
        if (!currentDistrict) {
            alert('Please fill the district field first.');
            return;
        }

        const district = currentDistrict;
        const soilData = DISTRICT_SOIL_DATA[district.toLowerCase()];
        if (!soilData) {
            alert(`District ${district} not supported for IoT data. Please use manual input.`);
            return;
        }

        // Add some random variation to simulate real sensor data
        const variation = () => (Math.random() - 0.5) * 0.2; // ±10% variation

        const variedPH = (soilData.ph * (1 + variation())).toFixed(1);
        const variedN = Math.round(soilData.nitrogen * (1 + variation()));
        const variedP = Math.round(soilData.phosphorus * (1 + variation()));
        const variedK = Math.round(soilData.potassium * (1 + variation()));
        const variedTemp = Math.round(soilData.temperature + (Math.random() - 0.5) * 4);
        const variedHumidity = Math.round(soilData.humidity + (Math.random() - 0.5) * 10);
        const variedRainfall = Math.round(soilData.rainfall * (1 + variation()));

        document.getElementById("ph").value = variedPH;
        document.getElementById("n").value = variedN;
        document.getElementById("p").value = variedP;
        document.getElementById("k").value = variedK;
        document.getElementById("temp").value = variedTemp;
        document.getElementById("moisture").value = variedHumidity;
        document.getElementById("rainfall").value = variedRainfall;
        document.getElementById("location").value = district;

        alert(`IoT Sensor Data Loaded (Simulated)!\n\nSoil Conditions:\n• pH: ${variedPH}\n• Nitrogen (N): ${variedN} kg/ha\n• Phosphorus (P): ${variedP} kg/ha\n• Potassium (K): ${variedK} kg/ha\n• Temperature: ${variedTemp}°C\n• Humidity: ${variedHumidity}%\n• Rainfall: ${variedRainfall} mm\n\nClick "Get AI Recommendation" to see crop suggestions.`);
    }
}

function checkConnectedSensors() {
    const sensorId = localStorage.getItem('connectedSensor');
    if (sensorId) {
        alert(`Connected IoT Sensor: ${sensorId}`);
    } else {
        alert('No IoT sensors connected. Please connect a sensor first.');
    }
}

function identifyDistrictFromCoords(lat, lon) {
    // Expanded coordinate-based district identification for Andhra Pradesh
    // Coastal Andhra districts (excluding Visakhapatnam)
    if (18.0 <= lat <= 19.5 && 82.5 <= lon <= 85.0) { // Northern coastal
        if (lon >= 84.0) return 'Srikakulam';
        else return 'Vizianagaram';
    } else if (16.0 <= lat <= 18.0 && 80.5 <= lon <= 83.0) {
        if (lat >= 17.0) return 'East Godavari';
        else return 'West Godavari';
    } else if (16.2 <= lat <= 16.8 && 80.0 <= lon <= 81.5) {
        return 'Krishna';
    } else if (15.5 <= lat <= 17.0 && 79.0 <= lon <= 81.5) {
        return 'Guntur';
    } else if (14.5 <= lat <= 16.5 && 78.0 <= lon <= 81.0) {
        return 'Prakasam';
    } else if (13.0 <= lat <= 16.0 && 78.0 <= lon <= 81.0) {
        return 'Nellore';
    }
    // Rayalaseema districts
    else if (13.5 <= lat <= 15.5 && 77.5 <= lon <= 79.5) {
        return 'Kadapa';
    } else if (13.5 <= lat <= 16.0 && 76.5 <= lon <= 78.5) {
        return 'Anantapur';
    } else if (15.0 <= lat <= 17.0 && 77.0 <= lon <= 79.5) {
        return 'Kurnool';
    } else if (12.5 <= lat <= 14.5 && 78.0 <= lon <= 80.5) {
        return 'Chittoor';
    }

    return null;
}

// Placeholder functions for export
function exportCropPDF() {
    alert('PDF export not implemented yet');
}

function exportCropCSV() {
    alert('CSV export not implemented yet');
}

function exportDiseasePDF() {
    alert('Disease PDF export not implemented yet');
}

// Placeholder functions for insights
function getSustainabilityScore() {
    document.getElementById('sustainability-result').innerHTML = 'Sustainability Score: 85% (Good)';
}

function getProfitForecast() {
    document.getElementById('profit-result').innerHTML = 'Estimated Profit: ₹45,000/ha';
}

function getRotationAdvice() {
    document.getElementById('rotation-result').innerHTML = 'Recommended: Rice → Wheat → Maize';
}

function getYieldPrediction() {
    document.getElementById('yield-result').innerHTML = 'Predicted Yield: 4.2 tons/ha';
}

// Crop recommendation
document.getElementById("crop-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    // Always read values from the form fields, regardless of input method
    let nitrogen = parseFloat(document.getElementById("n").value);
    let phosphorus = parseFloat(document.getElementById("p").value);
    let pH = parseFloat(document.getElementById("ph").value);
    let rainfall = parseFloat(document.getElementById("rainfall").value);
    let district = document.getElementById("location").value.trim();

    // Validate inputs
    if (!district) {
        document.getElementById("crop-result").innerHTML =
            "❌ Please enter district/location";
        return;
    }

    if (isNaN(nitrogen) || isNaN(phosphorus) || isNaN(pH) || isNaN(rainfall)) {
        document.getElementById("crop-result").innerHTML =
            "❌ Please enter valid numeric values for all soil parameters";
        return;
    }

    // Validate ranges
    if (pH < 4.0 || pH > 9.0) {
        document.getElementById("crop-result").innerHTML =
            "❌ pH must be between 4.0 and 9.0";
        return;
    }

    if (nitrogen < 0 || nitrogen > 200) {
        document.getElementById("crop-result").innerHTML =
            "❌ Nitrogen must be between 0 and 200 kg/ha";
        return;
    }

    if (phosphorus < 0 || phosphorus > 200) {
        document.getElementById("crop-result").innerHTML =
            "❌ Phosphorus must be between 0 and 200 kg/ha";
        return;
    }

    if (rainfall < 0 || rainfall > 3000) {
        document.getElementById("crop-result").innerHTML =
            "❌ Rainfall must be between 0 and 3000 mm";
        return;
    }

    const payload = {
        district: district,
        nitrogen: nitrogen,
        phosphorus: phosphorus,
        pH: pH,
        rainfall: rainfall
    };

    console.log("📤 Sending payload:", payload);

    try {
        const res = await fetch(`${CROP_API_BASE_URL}/api/recommend_crop`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const text = await res.text();
            throw new Error(`Backend error ${res.status}: ${text}`);
        }

        const response = await res.json();
        console.log("📥 Received response:", response);

        if (!response.data || !Array.isArray(response.data)) {
            throw new Error("Invalid backend response format");
        }

        const result = response.data[0];

        // Store the manual recommendation for the district
        const manualRecommendations = JSON.parse(localStorage.getItem('manualRecommendations') || '{}');
        manualRecommendations[district.toLowerCase()] = result.recommendation;
        localStorage.setItem('manualRecommendations', JSON.stringify(manualRecommendations));

        document.getElementById("crop-result").innerHTML = `
            ✅ <b>Recommended Crop for ${district}:</b> ${result.recommendation} (Accuracy: ${result.accuracy})
        `;

        document.getElementById("crop-export-buttons").style.display = "block";

    } catch (err) {
        console.error(err);
        document.getElementById("crop-result").innerHTML =
            `❌ Error: ${err.message}`;
        document.getElementById("crop-export-buttons").style.display = "none";
    }
});

// Disease Detection
document.getElementById("analyze-disease-btn").addEventListener("click", async (e) => {

    const imageInput = document.getElementById("image");
    const cropType = document.getElementById("crop-type").value.trim();

    if (!imageInput.files || imageInput.files.length === 0) {
        document.getElementById("disease-result").innerHTML =
            "❌ Please select an image file";
        return;
    }

    const file = imageInput.files[0];

    // Validate file type
    if (!file.type.startsWith('image/')) {
        document.getElementById("disease-result").innerHTML =
            "❌ Please select a valid image file";
        return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        document.getElementById("disease-result").innerHTML =
            "❌ File size must be less than 5MB";
        return;
    }

    // Show loading state
    document.getElementById("disease-result").innerHTML =
        "🔄 Analyzing image... Please wait.";
    document.getElementById("analyze-disease-btn").disabled = true;
    document.getElementById("analyze-disease-btn").textContent = "🔬 Analyzing...";

    try {
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('image', file);
        if (cropType) {
            formData.append('crop_type', cropType);
        }

        // Call the disease detection API
        const response = await fetch(`${DISEASE_API_BASE_URL}/api/detect_disease`, {
            method: 'POST',
            body: formData
        });

        // Read response body only once
        const responseText = await response.text();
        let result;

        if (!response.ok) {
            // Try to parse the response text as JSON for error details
            try {
                const errorData = JSON.parse(responseText);
                throw new Error(errorData.error || `HTTP ${response.status}`);
            } catch (jsonError) {
                // If JSON parsing fails, use the raw text
                throw new Error(`HTTP ${response.status}: ${responseText.substring(0, 200)}`);
            }
        }

        // Parse successful response
        try {
            result = JSON.parse(responseText);
        } catch (parseError) {
            throw new Error(`Invalid JSON response: ${responseText.substring(0, 200)}`);
        }

        if (!result.data) {
            throw new Error('Invalid response format');
        }

        const prediction = result.data.prediction;
        const confidence = result.data.confidence;
        const suggestions = result.data.suggestions || {};

        let resultHTML = `
            <div class="disease-result-card">
                <h3>🔍 Disease Detection Result</h3>
                <div class="prediction-main">
                    <strong>Disease:</strong> ${prediction}<br>
                    <strong>Confidence:</strong> ${(confidence * 100).toFixed(1)}%<br>
                    <strong>Crop Type:</strong> ${result.data.crop_type || 'Unknown'}<br>
                    <strong>Model:</strong> ${result.data.model_used || 'Unknown'}
                </div>
        `;

        // Handle treatment suggestions with proper error checking
        if (suggestions && typeof suggestions === 'object' && !Array.isArray(suggestions)) {
            if (prediction !== 'Healthy') {
                resultHTML += `<div class="treatment-suggestions">`;

                // Immediate actions
                if (suggestions.immediate_actions && Array.isArray(suggestions.immediate_actions) && suggestions.immediate_actions.length > 0) {
                    resultHTML += `
                        <h4>🚨 Immediate Actions Required:</h4>
                        <ul>
                            ${suggestions.immediate_actions.map(action => `<li>${action}</li>`).join('')}
                        </ul>
                    `;
                }

                // Preventive measures
                if (suggestions.preventive_measures && Array.isArray(suggestions.preventive_measures) && suggestions.preventive_measures.length > 0) {
                    resultHTML += `
                        <h4>🛡️ Preventive Measures:</h4>
                        <ul>
                            ${suggestions.preventive_measures.map(measure => `<li>${measure}</li>`).join('')}
                        </ul>
                    `;
                }

                // Treatment options (check for different possible keys)
                const organicOptions = suggestions.organic_options || suggestions.organic_treatments || suggestions.recommended_treatments;
                if (organicOptions && Array.isArray(organicOptions) && organicOptions.length > 0) {
                    resultHTML += `
                        <h4>🌱 Organic Treatment Options:</h4>
                        <ul>
                            ${organicOptions.map(treatment => `<li>${treatment}</li>`).join('')}
                        </ul>
                    `;
                }

                const chemicalOptions = suggestions.chemical_options || suggestions.chemical_treatments;
                if (chemicalOptions && Array.isArray(chemicalOptions) && chemicalOptions.length > 0) {
                    resultHTML += `
                        <h4>⚗️ Chemical Treatment Options:</h4>
                        <ul>
                            ${chemicalOptions.map(treatment => `<li>${treatment}</li>`).join('')}
                        </ul>
                    `;
                }

                // Handle error case for unknown diseases
                if (suggestions.error && suggestions.general_advice && Array.isArray(suggestions.general_advice)) {
                    resultHTML += `
                        <h4>ℹ️ General Advice:</h4>
                        <ul>
                            ${suggestions.general_advice.map(advice => `<li>${advice}</li>`).join('')}
                        </ul>
                    `;
                }

                resultHTML += `</div>`;
            } else if (prediction === 'Healthy') {
                resultHTML += `<div class="treatment-suggestions">`;
                resultHTML += `<h4>✅ Plant Health Status: Excellent!</h4>`;

                // Maintenance tips
                if (suggestions.maintenance_tips && Array.isArray(suggestions.maintenance_tips) && suggestions.maintenance_tips.length > 0) {
                    resultHTML += `<h5>🛠️ Maintenance Tips:</h5><ul>`;
                    resultHTML += suggestions.maintenance_tips.map(tip => `<li>${tip}</li>`).join('');
                    resultHTML += `</ul>`;
                }

                // Prevention tips
                if (suggestions.prevention_tips && Array.isArray(suggestions.prevention_tips) && suggestions.prevention_tips.length > 0) {
                    resultHTML += `<h5>🛡️ Prevention Tips:</h5><ul>`;
                    resultHTML += suggestions.prevention_tips.map(tip => `<li>${tip}</li>`).join('');
                    resultHTML += `</ul>`;
                }

                // Monitoring advice
                if (suggestions.monitoring_advice && Array.isArray(suggestions.monitoring_advice) && suggestions.monitoring_advice.length > 0) {
                    resultHTML += `<h5>👁️ Monitoring Advice:</h5><ul>`;
                    resultHTML += suggestions.monitoring_advice.map(tip => `<li>${tip}</li>`).join('');
                    resultHTML += `</ul>`;
                }

                resultHTML += `</div>`;
            }
        } else {
            // Handle case where suggestions is not an object or is missing
            resultHTML += `<div class="treatment-suggestions">`;
            resultHTML += `<h4>ℹ️ Additional Information:</h4>`;
            resultHTML += `<p>No specific treatment suggestions available for this prediction.</p>`;
            resultHTML += `</div>`;
        }

        resultHTML += `
            </div>
            <div class="export-buttons" id="disease-export-buttons" style="display: block; margin-top: 15px;">
                <button onclick="exportDiseasePDF()" class="export-btn">📄 Export PDF</button>
            </div>
        `;

        document.getElementById("disease-result").innerHTML = resultHTML;

    } catch (error) {
        console.error('Disease detection error:', error);
        document.getElementById("disease-result").innerHTML =
            `❌ Error analyzing image: ${error.message}`;
    } finally {
        // Reset button state
        document.getElementById("analyze-disease-btn").disabled = false;
        document.getElementById("analyze-disease-btn").textContent = "🔬 Analyze Disease";
    }
});

// Weather Forecast
document.getElementById("weather-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const location = document.getElementById("weather-location").value.trim();

    if (!location) {
        document.getElementById("weather-result").innerHTML =
            "❌ Please enter a location";
        return;
    }

    // Show immediate dummy weather data
    const conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Clear'];
    const randomCondition = conditions[Math.floor(Math.random() * conditions.length)];
    const temperature = Math.floor(Math.random() * 15) + 20; // 20-35°C
    const humidity = Math.floor(Math.random() * 30) + 50; // 50-80%
    const windSpeed = Math.floor(Math.random() * 15) + 5; // 5-20 km/h
    const rainfall = Math.floor(Math.random() * 20); // 0-20mm

    document.getElementById("weather-result").innerHTML = `
        <div class="weather-result-card">
            <h3>🌤️ Weather Forecast for ${location}</h3>
            <div class="weather-info">
                <strong>Current Conditions:</strong> ${randomCondition}<br>
                <strong>Temperature:</strong> ${temperature}°C<br>
                <strong>Humidity:</strong> ${humidity}%<br>
                <strong>Wind Speed:</strong> ${windSpeed} km/h<br>
                <strong>Forecast:</strong> ${randomCondition} conditions expected for the next 5 days<br>
                <strong>Rainfall Probability:</strong> ${rainfall}%
            </div>
        </div>
    `;
});

// Market Prices
document.getElementById("market-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const commodity = document.getElementById("commodity").value;
    const marketLocation = document.getElementById("market-location").value.trim();

    if (!marketLocation) {
        document.getElementById("market-result").innerHTML =
            "❌ Please enter a market location";
        return;
    }

    // Show immediate dummy market data
    const prices = {
        rice: { min: 1800, max: 2200, avg: 2000 },
        wheat: { min: 1900, max: 2300, avg: 2100 },
        maize: { min: 1600, max: 1900, avg: 1750 },
        cotton: { min: 4500, max: 5200, avg: 4850 },
        sugarcane: { min: 2800, max: 3200, avg: 3000 },
        soybean: { min: 3500, max: 4000, avg: 3750 },
        barley: { min: 1700, max: 2000, avg: 1850 },
        potato: { min: 1200, max: 1500, avg: 1350 },
        tomato: { min: 800, max: 1200, avg: 1000 },
        onion: { min: 1500, max: 1800, avg: 1650 },
        groundnut: { min: 4800, max: 5500, avg: 5150 },
        mustard: { min: 4200, max: 4800, avg: 4500 },
        sunflower: { min: 3800, max: 4300, avg: 4050 }
    };

    const price = prices[commodity] || { min: 0, max: 0, avg: 0 };
    const trend = Math.random() > 0.5 ? '📈 Rising' : '📉 Falling';
    const change = Math.floor(Math.random() * 10) + 1;

    document.getElementById("market-result").innerHTML = `
        <div class="market-result-card">
            <h3>💰 Market Prices for ${commodity.charAt(0).toUpperCase() + commodity.slice(1)} in ${marketLocation}</h3>
            <div class="market-info">
                <strong>Minimum Price:</strong> ₹${price.min}/quintal<br>
                <strong>Maximum Price:</strong> ₹${price.max}/quintal<br>
                <strong>Average Price:</strong> ₹${price.avg}/quintal<br>
                <strong>Last Updated:</strong> Today<br>
                <strong>Trend:</strong> ${trend} (${change}% ${trend.includes('Rising') ? 'increase' : 'decrease'} from last week)
            </div>
        </div>
    `;
});

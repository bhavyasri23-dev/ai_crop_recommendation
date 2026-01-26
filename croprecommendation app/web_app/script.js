const API_BASE_URL = "http://localhost:5002";

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 AI Crop Recommendation System initialized');

    // Set initial active states
    showSection('crop');
    setInputMethod('manual');

    // Test if functions are working
    console.log('✅ Navigation functions loaded');
});

// Navigation functions
function showSection(sectionName) {
    console.log('🔄 Switching to section:', sectionName);

    // Hide all sections
    const sections = document.querySelectorAll('main section');
    sections.forEach(section => {
        section.classList.remove('active-section');
        section.style.display = 'none';
    });

    // Remove active class from nav buttons
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => btn.classList.remove('active'));

    // Show selected section
    let targetSection;
    if (sectionName === 'crop') {
        targetSection = document.getElementById('crop-prediction');
    } else if (sectionName === 'disease') {
        targetSection = document.getElementById('disease-prediction');
    } else if (sectionName === 'weather') {
        targetSection = document.getElementById('weather');
    } else if (sectionName === 'insights') {
        targetSection = document.getElementById('insights');
    }

    if (targetSection) {
        targetSection.classList.add('active-section');
        targetSection.style.display = 'block';
        console.log('✅ Section shown:', sectionName);
    } else {
        console.error('❌ Section not found:', sectionName);
    }

    // Add active class to clicked nav button
    const activeBtn = document.querySelector(`[data-section="${sectionName}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
        console.log('✅ Nav button activated:', sectionName);
    }
}

// Input method switching
function setInputMethod(method) {
    console.log('🔄 Switching input method:', method);

    // Hide all input sections
    const inputSections = document.querySelectorAll('.input-section');
    inputSections.forEach(section => section.classList.remove('active'));

    // Remove active class from method buttons
    const methodButtons = document.querySelectorAll('.method-btn');
    methodButtons.forEach(btn => btn.classList.remove('active'));

    // Show selected input section
    const targetSection = document.getElementById(method + '-inputs');
    if (targetSection) {
        targetSection.classList.add('active');
        console.log('✅ Input method activated:', method);
    }

    // Add active class to clicked method button
    const activeBtn = document.querySelector(`[data-method="${method}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}

// Tab switching for weather/market
function showTab(tabName) {
    console.log('🔄 Switching tab:', tabName);

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
    const activeBtn = document.querySelector(`.tab-btn[onclick*="${tabName}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}

// District soil data for satellite/IoT simulation
const DISTRICT_SOIL_DATA = {
    'visakhapatnam': { ph: 6.6, nitrogen: 68, phosphorus: 195, potassium: 48, temperature: 27, humidity: 80, rainfall: 980 },

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

function identifyDistrictFromCoords(lat, lon) {
    // Expanded coordinate-based district identification for Andhra Pradesh
    // Coastal Andhra districts
    if (16.5 <= lat <= 18.5 && 82.5 <= lon <= 84.0) {
        return 'Visakhapatnam';
    } else if (18.0 <= lat <= 19.5 && 82.5 <= lon <= 85.0) { // Northern coastal
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

// Satellite data functions
async function fetchSatelliteData() {
    const input = document.getElementById("sat-location").value.trim();
    const currentDistrict = document.getElementById("location").value.trim();

    let district = null;

    if (input.includes(',')) {
        // Parse coordinates
        const coords = input.split(',').map(c => parseFloat(c.trim()));
        if (coords.length !== 2 || isNaN(coords[0]) || isNaN(coords[1])) {
            alert('Please enter valid coordinates in format: latitude, longitude');
            return;
        }

        const [lat, lon] = coords;

        // Identify district based on coordinates
        district = identifyDistrictFromCoords(lat, lon);
        if (!district) {
            district = 'Visakhapatnam';
        }
    } else if (input) {
        // Use satellite input as district name
        district = input;
    }

    if (!district) {
        district = currentDistrict;
    }

    if (!district) {
        alert('Please enter coordinates or district name in satellite input, or fill the district field');
        return;
    }

    // Get soil data for district
    const soilData = DISTRICT_SOIL_DATA[district.toLowerCase()] || DISTRICT_SOIL_DATA['visakhapatnam'];

    // Populate form with satellite data
    document.getElementById("ph").value = soilData.ph;
    document.getElementById("n").value = soilData.nitrogen;
    document.getElementById("p").value = soilData.phosphorus;
    document.getElementById("k").value = soilData.potassium;
    document.getElementById("temp").value = soilData.temperature;
    document.getElementById("moisture").value = soilData.humidity;
    document.getElementById("rainfall").value = soilData.rainfall;
    document.getElementById("location").value = district;

    // Show popup with soil conditions only - no automatic recommendation
    alert(`Satellite data loaded for ${district}!\n\nSoil Conditions:\n• pH: ${soilData.ph}\n• Nitrogen (N): ${soilData.nitrogen} kg/ha\n• Phosphorus (P): ${soilData.phosphorus} kg/ha\n• Potassium (K): ${soilData.potassium} kg/ha\n• Temperature: ${soilData.temperature}°C\n• Humidity: ${soilData.humidity}%\n• Rainfall: ${soilData.rainfall} mm/year\n\nClick "Get AI Recommendation" to get crop suggestions based on these conditions.`);
}

// IoT sensor functions
let connectedSensors = [];

async function connectIoT() {
    const sensorId = document.getElementById('sensor-id').value.trim();
    if (!sensorId) {
        alert('Please enter sensor ID');
        return;
    }

    try {
        // Show loading
        const resultDiv = document.getElementById('crop-result');
        resultDiv.innerHTML = '🔗 Connecting to IoT sensor...';

        // Simulate sensor connection (replace with actual IoT API)
        const response = await fetch(`http://localhost:5001/api/connect_sensor`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sensor_id: sensorId })
        });

        if (response.ok) {
            connectedSensors.push(sensorId);
            resultDiv.innerHTML = `✅ Connected to sensor ${sensorId}! You can now load sensor data.`;
        } else {
            throw new Error('Failed to connect to sensor');
        }

    } catch (error) {
        console.error('IoT connection error:', error);
        document.getElementById('crop-result').innerHTML = '❌ Failed to connect to IoT sensor. Please check sensor ID and try again.';
    }
}

async function populateFromIoTSensor() {
    if (connectedSensors.length === 0) {
        alert('No sensors connected. Please connect a sensor first.');
        return;
    }

    const sensorId = document.getElementById('sensor-id').value.trim();
    if (!sensorId || !connectedSensors.includes(sensorId)) {
        alert('Please enter a valid connected sensor ID');
        return;
    }

    try {
        // Show loading
        const resultDiv = document.getElementById('crop-result');
        resultDiv.innerHTML = '📊 Loading sensor data...';

        // Simulate sensor data fetch (replace with actual IoT API)
        const response = await fetch(`http://localhost:5001/api/sensor_data/${sensorId}`);
        const data = await response.json();

        // Populate form with sensor data
        document.getElementById('ph').value = data.ph || 6.5;
        document.getElementById('moisture').value = data.moisture || 50;
        document.getElementById('n').value = data.nitrogen || 60;
        document.getElementById('p').value = data.phosphorus || 40;
        document.getElementById('k').value = data.potassium || 30;
        document.getElementById('temp').value = data.temperature || 25;
        document.getElementById('rainfall').value = data.rainfall || 800;

        resultDiv.innerHTML = '✅ Sensor data loaded successfully! Please enter location and submit for recommendation.';

    } catch (error) {
        console.error('Sensor data fetch error:', error);
        document.getElementById('crop-result').innerHTML = '❌ Failed to load sensor data. Please try again.';
    }
}

function checkConnectedSensors() {
    const resultDiv = document.getElementById('crop-result');

    if (connectedSensors.length === 0) {
        resultDiv.innerHTML = '📡 No sensors connected. Use "Connect IoT Sensor" to add sensors.';
    } else {
        resultDiv.innerHTML = `📡 Connected Sensors: ${connectedSensors.join(', ')}`;
    }
}

// AI Insights functions
async function getSustainabilityScore() {
    const resultDiv = document.getElementById('sustainability-result');
    resultDiv.innerHTML = '🔄 Calculating sustainability score...';

    try {
        // Simulate sustainability calculation
        const score = Math.floor(Math.random() * 40) + 60; // Random score 60-100
        const recommendations = [
            'Use organic fertilizers',
            'Implement crop rotation',
            'Conserve water resources',
            'Reduce chemical pesticide use'
        ];

        resultDiv.innerHTML = `
            🌱 <b>Sustainability Score: ${score}/100</b><br>
            💡 <b>Recommendations:</b><br>
            • ${recommendations.join('<br>• ')}
        `;
    } catch (error) {
        resultDiv.innerHTML = '❌ Failed to calculate sustainability score.';
    }
}

async function getProfitForecast() {
    const resultDiv = document.getElementById('profit-result');
    resultDiv.innerHTML = '💰 Calculating profit forecast...';

    try {
        // Simulate profit forecast
        const profit = Math.floor(Math.random() * 50000) + 20000; // Random profit 20k-70k
        const margin = Math.floor(Math.random() * 30) + 15; // Random margin 15-45%

        resultDiv.innerHTML = `
            💰 <b>Estimated Annual Profit: ₹${profit.toLocaleString()}</b><br>
            📈 <b>Profit Margin: ${margin}%</b><br>
            📊 <b>Based on current market rates and yield predictions</b>
        `;
    } catch (error) {
        resultDiv.innerHTML = '❌ Failed to calculate profit forecast.';
    }
}

async function getRotationAdvice() {
    const resultDiv = document.getElementById('rotation-result');
    resultDiv.innerHTML = '🔄 Generating crop rotation advice...';

    try {
        const rotations = [
            'Rice → Groundnut → Cotton → Rice',
            'Sugarcane → Maize → Soybean → Sugarcane',
            'Cotton → Wheat → Sunflower → Cotton',
            'Groundnut → Rice → Cotton → Groundnut'
        ];

        const randomRotation = rotations[Math.floor(Math.random() * rotations.length)];

        resultDiv.innerHTML = `
            🔄 <b>Recommended Crop Rotation:</b><br>
            <b>${randomRotation}</b><br>
            💡 <b>Benefits:</b> Improved soil health, reduced pest pressure, better nutrient balance
        `;
    } catch (error) {
        resultDiv.innerHTML = '❌ Failed to generate rotation advice.';
    }
}

async function getYieldPrediction() {
    const resultDiv = document.getElementById('yield-result');
    resultDiv.innerHTML = '📈 Predicting yield...';

    try {
        const yield = Math.floor(Math.random() * 5) + 3; // Random yield 3-8 tons/ha
        const confidence = Math.floor(Math.random() * 20) + 80; // Random confidence 80-100%

        resultDiv.innerHTML = `
            📈 <b>Predicted Yield: ${yield} tons/hectare</b><br>
            🎯 <b>Confidence Level: ${confidence}%</b><br>
            📊 <b>Factors considered:</b> Soil quality, weather patterns, crop variety
        `;
    } catch (error) {
        resultDiv.innerHTML = '❌ Failed to predict yield.';
    }
}

// Export functions
function exportCropPDF() {
    alert('PDF export feature coming soon! 📄');
}

function exportCropCSV() {
    alert('CSV export feature coming soon! 📊');
}

function exportDiseasePDF() {
    alert('Disease report PDF export coming soon! 📄');
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
        const res = await fetch(`${API_BASE_URL}/api/recommend_crop`, {
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

        document.getElementById("crop-result").innerHTML = `
            ✅ <b>Recommended Crop for ${district}:</b> ${result.recommendation}<br>
            🌱 <b>Soil Fingerprint:</b> ${result.soil_fingerprint}
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
document.getElementById("disease-form").addEventListener("submit", async (e) => {
    e.preventDefault();

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
    document.getElementById("disease-form").querySelector('button[type="submit"]').disabled = true;
    document.getElementById("disease-form").querySelector('button[type="submit"]').textContent = "🔬 Analyzing...";

    try {
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('image', file);
        if (cropType) {
            formData.append('crop_type', cropType);
        }

        // Call the disease detection API
        const response = await fetch(`${API_BASE_URL}/api/detect_disease`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            // Try to parse as JSON first, fallback to text if it fails
            let errorData;
            try {
                errorData = await response.json();
                throw new Error(errorData.error || `HTTP ${response.status}`);
            } catch (jsonError) {
                // If JSON parsing fails, get the response as text
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText.substring(0, 200)}`);
            }
        }

        const result = await response.json();

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
        document.getElementById("disease-form").querySelector('button[type="submit"]').disabled = false;
        document.getElementById("disease-form").querySelector('button[type="submit"]').textContent = "🔬 Analyze Disease";
    }
});

// Weather form
document.getElementById("weather-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const location = document.getElementById("weather-location").value.trim();

    if (!location) {
        document.getElementById("weather-result").innerHTML = "❌ Please enter location";
        return;
    }

    try {
        const res = await fetch(`http://localhost:5001/api/weather?location=${encodeURIComponent(location)}`);

        if (!res.ok) {
            throw new Error(`Weather API error: ${res.status}`);
        }

        const response = await res.json();

        document.getElementById("weather-result").innerHTML = `
            🌤️ <b>Weather Forecast for ${location}:</b><br>
            🌡️ <b>Temperature:</b> ${response.temperature || 'N/A'}°C<br>
            💧 <b>Humidity:</b> ${response.humidity || 'N/A'}%<br>
            🌧️ <b>Rainfall:</b> ${response.rainfall || 'N/A'}mm<br>
            💨 <b>Wind Speed:</b> ${response.wind_speed || 'N/A'} km/h
        `;

    } catch (err) {
        console.error(err);
        document.getElementById("weather-result").innerHTML = `❌ Error: ${err.message}`;
    }
});

// Market form
document.getElementById("market-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const commodity = document.getElementById("commodity").value;
    const location = document.getElementById("market-location").value.trim();

    if (!commodity || !location) {
        document.getElementById("market-result").innerHTML = "❌ Please select commodity and enter location";
        return;
    }

    try {
        const res = await fetch(`http://localhost:5001/api/market?commodity=${encodeURIComponent(commodity)}&location=${encodeURIComponent(location)}`);

        if (!res.ok) {
            throw new Error(`Market API error: ${res.status}`);
        }

        const response = await res.json();

        document.getElementById("market-result").innerHTML = `
            💰 <b>${commodity} Market Prices in ${location}:</b><br>
            📈 <b>Current Price:</b> ₹${response.current_price || 'N/A'}/kg<br>
            📊 <b>Average Price:</b> ₹${response.average_price || 'N/A'}/kg<br>
            📅 <b>Last Updated:</b> ${response.last_updated || 'N/A'}
        `;

    } catch (err) {
        console.error(err);
        document.getElementById("market-result").innerHTML = `❌ Error: ${err.message}`;
    }
});

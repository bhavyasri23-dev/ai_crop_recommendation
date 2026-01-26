import requests

url = 'http://localhost:5000/api/iot/connect_sensor'
data = {'sensor_id': 'SOIL_001', 'sensor_type': 'soil_sensor', 'protocol': 'mqtt'}
response = requests.post(url, json=data)
print(f'Status: {response.status_code}')
print(f'Response: {response.text}')

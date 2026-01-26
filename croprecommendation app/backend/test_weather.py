import requests

def test_weather_endpoint():
    # Test the weather endpoint
    try:
        response = requests.get('http://localhost:5000/get_weather?location=London')
        print(f"Weather endpoint status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to test weather endpoint: {e}")

if __name__ == '__main__':
    test_weather_endpoint()

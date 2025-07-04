import requests
from config import API_KEY, BASE_URL

def get_weather(city):
    """Fetching the weather data for a given city."""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric' # Use 'imperial' for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200: # error handling
        return response.json()
    else:
        return None
    
if __name__ == "__main__":
    city = input("Enter city name: ")
    data = get_weather(city)
    if data:
        print(f"🌤 Weather in {data['name']}, {data['sys']['country']}")
        print(f"🌡️ Temperature: {data['main']['temp']}°C")
        print(f"🤗 Feels like: {data['main']['feels_like']}°C")
        print(f"💧 Humidity: {data['main']['humidity']}%")
        print(f"🌈 Weather: {data['weather'][0]['description'].title()}")
        print(f"💨 Wind Speed: {data['wind']['speed']} m/s")
    else:
        print("Could not retrieve weather data. Please check the city name or try again later.")
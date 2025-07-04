import requests
from config import API_KEY, BASE_URL

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/" 
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    # Get current weather
    current = requests.get(base_url + "weather", params=params).json()
    if current.get("cod") != 200:
        return current

    # Get 5-day forecast
    forecast_resp = requests.get(base_url + "forecast", params=params).json()
    forecast = forecast_resp.get("list", [])

    # Combine both
    current["forecast"] = forecast
    return current

def get_coordinates(city):
    """Get coordinates for AQI"""
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": API_KEY}
    response = requests.get(geo_url, params=params)
    data = response.json()
    if data:
        return data[0]["lat"], data[0]["lon"]
    return None, None

def get_aqi(lat, lon):
    """Fetch Air Quality Index data"""
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    response = requests.get(url, params=params)
    return response.json()
    
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
import requests

class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_weather(self, city):
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        response = requests.get(self.BASE_URL, params=params)
        
        if response.status_code != 200:
            raise ValueError(f"Weather API error: {response.text}")
        
        return response.json()
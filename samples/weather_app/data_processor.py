import csv
from datetime import datetime

class WeatherDataProcessor:

    def __init__(self, weather_service):
        self.weather_service = weather_service
    
    def collect_city_weather(self, cities):
        weather_data = []
        
        for city in cities:
            try:
                weather = self.weather_service.get_weather(city)
                processed_data = {
                    'city': city,
                    'temperature': weather['main']['temp'],
                    'humidity': weather['main']['humidity'],
                    'timestamp': datetime.now().isoformat()
                }
                weather_data.append(processed_data)
            except Exception as e:
                print(f"Error fetching weather for {city}: {e}")
        
        return weather_data
    
    def export_to_csv(self, weather_data, filename):
        if not weather_data:
            return False
        
        keys = weather_data[0].keys()
        
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(weather_data)
        
        return True
    

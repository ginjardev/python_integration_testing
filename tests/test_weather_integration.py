import os
import pytest
import responses
from samples.weather_app.weather_service import WeatherService
from samples.weather_app.data_processor import WeatherDataProcessor
from conftest import set_test_status



@pytest.fixture
def mock_weather_service():
    # Use responses to mock external API calls
    weather_service = WeatherService(api_key='test_key')
    return weather_service

@responses.activate
def test_weather_data_collection(mock_weather_service, set_test_status):
    # Mock the OpenWeatherMap API response
    responses.add(
        responses.GET, 
        "https://api.openweathermap.org/data/2.5/weather",
        json={
            'main': {
                'temp': 20.5,
                'humidity': 65
            }
        },
        status=200
    )
    
    try:
        # Create processor with mocked service
        processor = WeatherDataProcessor(mock_weather_service)

        # Test data collection
        cities = ['London', 'New York', 'Tokyo']
        weather_data = processor.collect_city_weather(cities)

        assert len(weather_data) == 3
        assert all('temperature' in data for data in weather_data)
        assert all('humidity' in data for data in weather_data)
        set_test_status(status="passed", remark="API builds metadata returned")
    except AssertionError as e:
        set_test_status(status="failed", remark="API sessions metadata not returned")
        raise (e)



@responses.activate
def test_weather_data_export( mock_weather_service, tmp_path, set_test_status):
    # Mock API response
    responses.add(
        responses.GET, 
        "https://api.openweathermap.org/data/2.5/weather",
        json={
            'main': {
                'temp': 20.5,
                'humidity': 65
            }
        },
        status=200
    )
    
    try:
        processor = WeatherDataProcessor(mock_weather_service)

        cities = ['London']
        weather_data = processor.collect_city_weather(cities)

        # Export to temporary CSV
        output_file = tmp_path / "weather_data.csv"
        result = processor.export_to_csv(weather_data, output_file)

        assert result is True
        assert os.path.exists(output_file)

        # Verify CSV contents
        with open(output_file, 'r') as f:
            lines = f.readlines()
            # Header + data
            assert len(lines) == 2  
        set_test_status(status="passed", remark="API builds metadata returned")
    except AssertionError as e:
        set_test_status(status="failed", remark="API sessions metadata not returned")
        raise (e)
        

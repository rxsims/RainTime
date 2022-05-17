import requests
from airflow.decorators import task



@task()
def forecast_urls(latitude: float, longitude: float) -> dict:
    # Take some input coordinates and find the appropriate grid location, associated urls, and radar station id
    base_url = 'https://api.weather.gov/points/'
    grid_url = f'{base_url}{latitude:.3f}%2C{longitude:.3f}'

    r = requests.get(grid_url)
    url_data = r.json()['properties']

    radar_dict = {
        'radarStation': url_data['radarStation'],   # Radar Station ID
        'grid': url_data['forecastGridData'],       # Grid level data: precise data on many meteorological features but inconsistent times
        'forecast': url_data['forecast'],           # Twice-daily forecast data
        'hourly': url_data['forecastHourly']        # Hourly forecast data
    }
    
    return radar_dict
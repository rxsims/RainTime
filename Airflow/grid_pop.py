import requests
from datetime import datetime, timedelta
from airflow.decorators import task
import time


@task()
def max_pop(grid_url, threshold_pop=50, time_window=timedelta(hours=6)):
    grid_url = grid_url['grid']

    # Set maximum forecast time
    start_time = datetime.now()
    final_time = start_time + time_window

    # This call frequently gets timed out, so explicitly rerun after a short wait if this happens
    r_grid = requests.get(grid_url)
    if r_grid.status_code == 200:
        print(f'URL: {grid_url}')
        print('Grid Data received...')
    else: 
        print('Data not received... Trying again.')
        time.sleep(5)
        r_grid = requests.get(grid_url)
    pop_data = r_grid.json()['properties']['probabilityOfPrecipitation']

    """
    Check for whether the probability exceeds the threshold value before the end of the forecast window.
    Either exceeding the probability threshold or reaching the end of the window is sufficient to end the search.
    If threshold is not reached, find the maximum value of the probability.
    """
    likely_percip = False
    max_pop_val = 0
    for pop_at_time in pop_data['values']:
        # Check that the report times and timezones are consistent
        time_str, timezone_w_delay = pop_at_time['validTime'].split('+')
        time_dt = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')

        if timezone_w_delay[:5] != '00:00':
            print(f'Different timezone at {time_dt}')

        # Update current maximum value for the PoP
        max_pop_val = max(max_pop_val, pop_at_time['value'])
        
        # Check threshold value for PoP
        if max_pop_val >= threshold_pop:
            print(f'Threshold Probability {threshold_pop}% reached...')
            likely_percip = True
            break
        
        # Check if time window is exceeded.
        if time_dt > final_time:
            print('Time limit exceeded...')
            print(f'Maximum Forecast Probability: {max_pop_val}')
            break

    return {'pop_max': max_pop_val, 'threshold_reach':likely_percip}
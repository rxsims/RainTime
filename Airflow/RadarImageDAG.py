from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import dag

from coord_urls import forecast_urls
from grid_pop import max_pop
from download_image_logic import image_decision
from radar_img import get_image

default_args={
    'retries': 0,
    'retry_delay': timedelta(seconds=30)
}

@dag(
    default_args=default_args,
    start_date = datetime(2022,5,16),
    schedule_interval=timedelta(minutes=5),
    catchup=False,
    tags=['meteorology']
)
def GetRadarImages():
    radar_dict = forecast_urls(42, -71)  # Latitude and Longitude of Point of Interest

    pop_dict = max_pop(
        grid_url = radar_dict,
        threshold_pop = 50,
        time_window = timedelta(hours=6)
    )
    
    img_dict = image_decision(
        pop_dict,
        radar_dict,
        floor_val = 20
    )

    get_image(img_dict)


a = GetRadarImages()
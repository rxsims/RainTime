import os
import requests
from bs4 import BeautifulSoup
from airflow.decorators import task



@task()
def image_decision(pop_dict, radar_station_id, floor_val=20):
    radar_station_id = radar_station_id['radarStation']
    # Different radar (other than BREF-RAW) are available, but this is sufficient for now.
    img_url = f'https://mrms.ncep.noaa.gov/data/RIDGEII/L2/{radar_station_id}/BREF_RAW/'

    to_download = False

    # Check whether the ceiling or floor values for the probability have been reached
    # If so, return output from the PoP search
    pop_max = pop_dict['pop_max']
    if pop_max < floor_val or pop_dict['threshold_reach']:
        print('Good to pass...')
        to_download = pop_dict['threshold_reach']


    # Create the directories needed later if they do not exist
    if not os.path.exists('images'):
        os.makedirs('gz_dl') # Directory to download the .gz radar files
        os.makedirs('images') # Directory to store the uncompressed images

        
    # Get all radar image links
    r_html = requests.get(img_url)
    soup = BeautifulSoup(r_html.content, 'html.parser')
    

    # Check if the most recent radar image has already been downloaded
    # If so, do not download it again
    most_recent_img = soup.find_all('a', href=True)[-1]['href']
    if most_recent_img in os.listdir('gz_dl') and to_download:
        print('Nothing new here.')
        to_download = False

    return {'to_download': to_download, 'img_url':img_url+most_recent_img}
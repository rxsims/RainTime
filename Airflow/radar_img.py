import requests
from airflow.decorators import task



@task()
def get_image(img_url):
    if img_url['to_download']:
        img_url = img_url['img_url']
        file_name = img_url.split('/')[-1]
        print(f'File: {file_name}')

        # Download and save compressed file    
        radar_image_comp = requests.get(img_url, stream=True)
        print(f'Downloading...')
        with open(f'./gz_dl/{file_name}', 'wb') as f:
            for chunk in radar_image_comp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        f.close()
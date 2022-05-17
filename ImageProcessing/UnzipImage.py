from PIL import Image
import gzip
import os
import io

def unzip_img(path):
    with gzip.open(path) as f:
        img = Image.open(io.BytesIO(f.read()))
    f.close()
    return img
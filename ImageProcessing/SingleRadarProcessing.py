import numpy as np
from ImgToDBZ import RGB_to_DBZ


class RadarProcessing:
    """
    Single Radar Image processing
    """
    def __init__(self, image, bbox_coords, color_process):
        self.color_process = color_process
        self.bbox_coords = bbox_coords
        self.img_size = image.size
        self.img_mask = self.thres_mask(image)
    
    """
    From an Image, use color processing class to find nearest DBZ values for each pixel.
    If the DBZ values falls below a threshold value, zero out the pixel value.
    """
    def set_thres_on_image(self, image):
        binned_colors, _ = self.color_process.convert_img_to_centers(image)
        return self.color_process.zero_below_thres(binned_colors)
    
    
    """
    Create a mask of the image: 1 above the threshold, 0 below.
    """
    def thres_mask(self, image):
        return np.where(self.set_thres_on_image(image)!=0, 1, 0)
    
    
    """
    Return a array of all (x,y) pixel-coordinates for the image mask
    """
    def mask_coords(self):
        return np.argwhere(self.img_mask==1)[:,::-1]
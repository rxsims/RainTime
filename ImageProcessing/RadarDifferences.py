import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

from SingleRadarProcessing import RadarProcessing
from VectorMath import *


class RadarDifference:
    """
    """
    def __init__(self, image_before, image_after, bbox_coords, color_process):
        if image_before.size != image_after.size:
            print('The two images are not the same size.  Additional pre-processing needed.')
            return None
        
        self.color_process = color_process
        self.bbox_coords = bbox_coords
        self.before_img = RadarProcessing(image_before, bbox_coords, color_process)
        self.after_img = RadarProcessing(image_after, bbox_coords, color_process)
        
        self.diff_mask = self.masked_difference().reshape(self.before_img.img_size)
        self.bef_only_coords = np.argwhere(self.diff_mask==0)[:,::-1]
        self.aft_only_coords = np.argwhere(self.diff_mask==2)[:,::-1]
        self.bef_only_cent = self.bef_only_coords.mean(axis=0)
        self.aft_only_cent = self.aft_only_coords.mean(axis=0)

        
    """
    Calculates the difference between the before and after image masks.
    0 -> Before Only
    1 -> No change (Above or Below threshold on both images)
    2 -> After Only
    """
    def masked_difference(self):
        return self.after_img.img_mask - self.before_img.img_mask + 1
    
    
    """
    Return the displacement vector of the Center of Mass from before-only to after-only pixels
    """
    def com_displacement(self):
        return directional_vector(self.bef_only_cent, self.aft_only_cent)
    
    
    """
    Display the difference in two radar images
    """
    def display_img_diff(self, fig_size=(6,6)):
        color_array = np.array([
            [0,0,255],[255,255,255],[255,0,0]
        ])
        
        fig, ax = plt.subplots(figsize=fig_size)
        ax.imshow(Image.fromarray(np.uint8(color_array[self.diff_mask])))
        plt.show()
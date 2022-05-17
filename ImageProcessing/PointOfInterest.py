import numpy as np
from SphericalCoordMath import *
from VectorMath import *


class POI:
    """
    Define a Point of Interest by the pixel-coordinates of interest, as well as the geographic bounding box of the image.
    Image size allows us to convert between geographic and pixel coordinates.
    Angular and distance (radial) bins are created, and normalization factors for bins are found.
    """
    def __init__(self, poi_coords, bbox_coords, img_size, dangle=5., ddist=0.002):
        self.coords = poi_coords
        self.bbox_coords = bbox_coords
        self.img_size = img_size
        
        self.angular_bins = np.arange(-180, 180+dangle, dangle)
        self.distance_bins = np.arange(0, 0.2+ddist, ddist)
        
        self.max_in_bins = self.find_bin_norms()
        
        
    """
    Create a coordinate mesh for the image.
    Remove the individual point of interest from the mesh (no zero-distance points).
    """
    def image_mesh(self):
        width_array = np.arange(0, self.img_size[0], 1)
        height_array = np.arange(0, self.img_size[1], 1)
        full_mesh = np.concatenate([
            np.repeat(width_array, self.img_size[1]).reshape(-1,1),
            np.tile(height_array, self.img_size[0]).reshape(-1,1)
        ], axis=1)
        full_mesh = np.delete(full_mesh, np.argwhere((full_mesh==self.coords).all(axis=1)), axis=0)
        
        return full_mesh
    
    
    """
    Take array of image-pixel coordinates and calculate the number of points in each of the 2d-bins
    """    
    def bin_image(self, img_proc, is_norm=False):
        img_angles = self.find_true_angle(img_proc)
        img_dist = self.find_dist(img_proc)
        
        binned_img, _, _ = np.histogram2d(img_angles, img_dist, bins=[self.angular_bins,self.distance_bins])
        if is_norm:
            binned_img = np.divide(binned_img, self.max_in_bins, out=np.zeros_like(self.max_in_bins), where=(self.max_in_bins!=0))
        return binned_img
    

    """
    Find the maximum number of points in the image that can be in each angular & distance bin.
    Found by sending all points in an image, except the PoI coordinates.
    """
    def find_bin_norms(self):
        mesh = self.image_mesh()
        return self.bin_image(mesh)
    
    
    """
    Find the (true) angle from the PoI to an array of coordinates
    """
    def find_true_angle(self, coords_arr):
        _, norm_vec = directional_vector(self.coords, coords_arr)
        angle_cos = 180/np.pi * np.arccos(norm_vec[:,0])
        angle_true = (-1)**(norm_vec[:,1]<0) * angle_cos
        return angle_true
    
    
    """
    Find (central angle) distance between the PoI and an array of coordinates
    """
    def find_dist(self, coords_arr):
        return dist_sph_from_pixels(*self.coords, *coords_arr.T, self.bbox_coords, *self.img_size)
    
    
    """
    Given an array of angles, find the (right-indexed) bin number for each angle.
    Note, if the angle of interest is 180, this is degenerate with -180, but should be in the final bin.
    """
    def digitize_angles(self, angle_arr):
        return np.digitize(np.where(angle_arr==180, 179.99, angle_arr), bins=self.angular_bins)
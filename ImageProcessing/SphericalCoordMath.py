import numpy as np

def spherical_from_pixel(x,y, bbox_coords, width, height):
    dlongitude = x/width*(bbox_coords[1] - bbox_coords[0])
    dlatitude = y/height*(bbox_coords[2] - bbox_coords[3])
    
    return [dlongitude+bbox_coords[0], dlatitude+bbox_coords[3]]


def dist_sph_from_coords(long1,lat1, long2,lat2):
    dlong = np.pi/180*(long1 - long2)
    dlat = np.pi/180*(lat1 - lat2)
    
    central_angle = 2*np.arcsin(np.sqrt(
        np.sin(dlat/2)**2
        + (1-np.sin(dlat/2)**2 - np.sin(np.pi/180*(lat1 + lat2)/2)**2)
        *np.sin(dlong/2)**2))
    return central_angle


def dist_sph_from_pixels(x1,y1, x2,y2, bbox_coords, width, height):
    long1,lat1 = spherical_from_pixel(x1,y1, bbox_coords, width, height)
    long2,lat2 = spherical_from_pixel(x2,y2, bbox_coords, width, height)
    return dist_sph_from_coords(long1,lat1, long2,lat2)
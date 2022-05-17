from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
import numpy as np
import pandas as pd


class RGB_to_DBZ:
    def __init__(self, thres_dbz = 20.):
        self.transform_file = pd.read_csv('./ColorLegend.csv')
        self.rgb_centers = np.ascontiguousarray(self.transform_file[['R','G','B']].values) # KMeans requires(?) contiguous
        self.thres_id = self.transform_file.query('dBZ >= @thres_dbz').index[0]
        self.find_center = self.create_KMeans()
    
    
    def create_KMeans(self):
        approx_dbz = KMeans(n_clusters=len(self.rgb_centers),n_init=1, random_state=0)
        approx_dbz.fit(self.rgb_centers)
        approx_dbz.cluster_centers_ = self.rgb_centers.astype(float)
        return approx_dbz
    
    
    def display_centers(self):
        center_ints = np.uint8(self.find_center.cluster_centers_)
        fig,ax = plt.subplots(figsize=(10,0.5))
        for i, color in enumerate(center_ints[1:]):
            ax.add_patch(Rectangle((self.transform_file.iloc[i, 3],0),1,1, color=color/256))
        ax.set_xlabel('Approximate dBZ')
        plt.xlim(self.transform_file['dBZ'].min(), self.transform_file['dBZ'].max())
        plt.yticks([])
        plt.show()
        
        
    def convert_img_to_centers(self, img):
        size = img.size
        img_arr = np.asarray(img)[...,:3].reshape((-1,3))
        img_bin = self.find_center.predict(img_arr)
        return (img_bin, size)
    
    
    def img_from_bin(self, bin_arr, size):
        return Image.fromarray(np.uint8(self.rgb_centers[bin_arr]).reshape((*size,3)))
    
    
    def zero_below_thres(self, bin_arr):
        return np.where(bin_arr<self.thres_id, 0, bin_arr)
    
    
    def zero_above_thres(self, bin_arr):
        return np.where(bin_arr<self.thres_id, bin_arr, 0)
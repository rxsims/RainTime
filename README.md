# RainTime
Calculate approximate time for precipitation at a given location based on NOAA radar images.


### Image Processing
Main image (pre)processing files to find where the precipitation is actually reaching the ground (set by some threshold value) and remove radar artifacts that pollute the images. A Jupyter Notebook is also included to show an example of how the images can be used to produce a normalized, binned data set with which the rain arrival time will be calculated.

### Airflow
Contains all necessary files for a simple DAG (using the TaskFlow API) to pull the relevant NOAA radar image for a particular geographic location when the probability of precipitation (PoP) is above a threshold value.  Will eventually be expanded to include image processing task and estimate time of arrival of rain storms at the given location.

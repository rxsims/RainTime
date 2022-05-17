# RainTime
Calculate approximate time for precipitation at a given location based on NOAA radar images.


## Image Processing
Main image (pre)processing files to find where the precipitation is actually reaching the ground (set by some threshold value) and remove radar artifacts that pollute the images.

## Airflow
Contains all necessary files for a simple DAG (using the TaskFlow API) to pull the relevant NOAA radar image for a particular geographic location.


# coding: utf-8

# In[1]:

""" Convert hyde asc rasters to geotiff
-------------------------------------------------------------------------------


Author: Rutger Hofste
Date: 20190722
Kernel: python35
Docker: rutgerhofste/gisdocker:ubuntu16.04

"""


SCRIPT_NAME = "Y2019M07D22_RH_Hyde_Convert_Geotiff_V01"
OUTPUT_VERSION = 1

S3_INPUT_PATH = "s3://wri-projects/Aqueduct30/rawData/Hyde/hyde3.2/baseline/unzipped/"

ec2_input_path = "/volumes/data/{}/input_V{:02.0f}/".format(SCRIPT_NAME,OUTPUT_VERSION)
ec2_output_path = "/volumes/data/{}/output_V{:02.0f}/".format(SCRIPT_NAME,OUTPUT_VERSION)

s3_output_path = "s3://wri-projects/Aqueduct30/processData/{}/output_V{:02.0f}/".format(SCRIPT_NAME,OUTPUT_VERSION)

gcs_output_path = "gs://aqueduct30_v01/{}/output_V{:02.0f}/".format(SCRIPT_NAME,OUTPUT_VERSION)

print(gcs_output_path,s3_output_path)


# In[2]:

import time, datetime, sys
dateString = time.strftime("Y%YM%mD%d")
timeString = time.strftime("UTC %H:%M")
start = datetime.datetime.now()
print(dateString,timeString)
sys.version


# In[3]:

#!rm -r {ec2_input_path}
get_ipython().system('rm -r {ec2_output_path}')

get_ipython().system('mkdir -p {ec2_input_path}')
get_ipython().system('mkdir -p {ec2_output_path}')


# In[4]:

import os
import rasterio
from tqdm import tqdm


# In[5]:

get_ipython().system('aws s3 sync {S3_INPUT_PATH} {ec2_input_path} ')


# In[6]:

paths = []
for root, dirs, files in os.walk(ec2_input_path):
    for file in files:
        if file.endswith(".asc"):
             paths.append(os.path.join(root, file))


# In[7]:

def raster_to_geotiff(src_path,dst_path):
    """ Opens a rasterio single band raster and 
    converts to LZW compressed geotiff. 
    
    dType and projection are preserved.
    
    Args:
        src_path(string): input file path.
        dst_path(string): output file path.
    
    """
    with rasterio.open(src_path) as src:
        profile = src.profile
        profile.update(nodata=-9999,
                       compress='lzw')
        
        if src.crs is None:
            crs = rasterio.crs.CRS.from_dict(init='epsg:4326')
        else:
            crs = src.crs
        
        with rasterio.open(
            dst_path,
            'w',
            driver='GTiff',
            height=src.height,
            width=src.width,
            count=1,
            dtype=src.dtypes[0],
            crs=crs,
            nodata = src.nodata,
            transform=src.transform,
        ) as dst:
            dst.write(src.read(1), 1)
    return dst_path


# In[ ]:

for path in tqdm(paths):
    input_filename = path.split("/")[-1]
    base_filename, input_extension = input_filename.split(".")
    output_filename = base_filename + ".tif"
    output_path = ec2_output_path + output_filename
    raster_to_geotiff(path,output_path)


# In[ ]:

get_ipython().system('gsutil -m cp -r {ec2_output_path} {gcs_output_path}')


# In[ ]:

get_ipython().system('aws s3 cp --recursive {ec2_output_path}  {s3_output_path} ')


# In[ ]:

end = datetime.datetime.now()
elapsed = end - start
print(elapsed)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




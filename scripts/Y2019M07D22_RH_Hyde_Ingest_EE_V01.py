
# coding: utf-8

# In[1]:

""" Ingest the Hyde geotiff data into Google Earth Engine. 
-------------------------------------------------------------------------------

Author: Rutger Hofste
Date: 20190722
Kernel: python35
Docker: rutgerhofste/gisdocker:ubuntu16.04

"""

TESTING = 0

SCRIPT_NAME = "Y2019M07D22_RH_Hyde_Ingest_EE_V01"
OUTPUT_VERSION = 1

NODATA_VALUE = -9999

GCS_BUCKET = "aqueduct30_v01"
PREFIX = "Y2019M07D22_RH_Hyde_Convert_Geotiff_V01"

EE_OUTPUT_PATH = "projects/WRI-Aquaduct/Y2019M07D22_RH_Hyde_Ingest_EE_V01"

EXTRA_PARAMS = {"script_name":SCRIPT_NAME,
                "output_version":OUTPUT_VERSION,
                "scenario":"Baseline estimate",
                "github":"https://github.com/rutgerhofste/hyde",
                "ingested_by":"Rutger Hofste"}

URL_POP_METADATA = "https://raw.githubusercontent.com/rutgerhofste/hyde/master/data/pop.csv"
URL_LU_METADATA = "https://raw.githubusercontent.com/rutgerhofste/hyde/master/data/lu.csv"


# In[2]:

import time, datetime, sys
dateString = time.strftime("Y%YM%mD%d")
timeString = time.strftime("UTC %H:%M")
start = datetime.datetime.now()
print(dateString,timeString)
sys.version


# In[3]:

import os
import subprocess
from tqdm import tqdm
import pandas as pd
from google.cloud import storage


# In[4]:

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/.google.json"


# In[5]:

df_pop = pd.read_csv(URL_POP_METADATA)


# In[6]:

df_lu = pd.read_csv(URL_LU_METADATA)


# In[7]:

def numeric_to_string(year):
    """
    Convert numeric year to string
    """
    if year < 0 :
          yearstring = "{}BC".format(year*-1)
    elif year >= 0:
          yearstring = "{}AD".format(year)
    else:
          raise
    return yearstring



def get_years_dict():
    Y_BCE = list(range(-10000,0,1000))
    Y_BCE_1700 = list(range(0,1700,100))
    Y_1700_2000 = list(range(1700,2000,10))
    Y_2000_2017 = list(range(2000,2017+1,1))
    years = Y_BCE + Y_BCE_1700 + Y_1700_2000 + Y_2000_2017
    year_strings = map(numeric_to_string,years)
    years_dict =  dict(zip(year_strings ,years))
    return years_dict


def dictionary_to_EE_upload_command(d):
    """ Convert a dictionary to command that can be appended to upload command
    -------------------------------------------------------------------------------
     
    
    Args:
        d (dictionary) : Dictionary with metadata. nodata_value                         
    
    Returns:
        command (string) : string to append to upload string.    
    
    """
    command = ""
    for key, value in d.items():            
        if key == "nodata_value":
            command = command + " --nodata_value={}".format(value)
        else:
            
            if isinstance(value, str):
                command = command + " -p '(string){}={}'".format(key,value)
            else:
                command = command + " -p '(number){}={}'".format(key,value)
                
    return command



def get_command(structure,filename,description,year,year_string):
        if structure == "pop":
            filename = "{}_{}.tif".format(filename,year_string)
        elif structure == "lu":
            filename = "{}{}.tif".format(filename,year_string)
        else:
            raise
        params = {"year":year,
                  "year_string":year_string,
                  "description":description,
                  "type":row.filename}
        params = {**params , **EXTRA_PARAMS}
        params["nodata_value"] = NODATA_VALUE
        meta_command = dictionary_to_EE_upload_command(params) 
        
        output_ic_name = "hyde321v01"
        base, extension = filename.split(".")
        image_name = base
        destination_path = "{}/output_V{:02d}/{}/{}".format(EE_OUTPUT_PATH,OUTPUT_VERSION,output_ic_name,image_name)
        source_path = "gs://aqueduct30_v01/{}//output_V01/output_V01/{}".format(PREFIX,filename)
        command = "/opt/anaconda3/envs/python35/bin/earthengine upload image --asset_id={} {} {}".format(destination_path,meta_command,source_path)

        return command


# In[8]:

commands = []
years_dict = get_years_dict()
for year_string, year in years_dict.items():
    for description, row in df_pop.iterrows():
        structure = "pop"
        filename = row.filename
        description = row.description
        command = get_command(structure,filename,description,year,year_string)
        commands.append(command)

        
    for description, row in df_lu.iterrows():
        structure = "lu"
        filename = row.filename
        description = row.description
        command = get_command(structure,filename,description,year,year_string)
        commands.append(command)


# In[9]:

if TESTING:
    commands = commands[0:3]


# In[ ]:

for command in tqdm(commands):
    subprocess.check_output(command,shell=True)
    


# In[ ]:

end = datetime.datetime.now()
elapsed = end - start
print(elapsed)


# In[ ]:




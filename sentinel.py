# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 15:15:41 2021

@author: Kostas-Geosystems
"""
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
from datetime import datetime
import geopandas
import pandas as pd 
import datetime
import configparser
from dateutil import parser
import time

### Parse the credentials ######
config = configparser.ConfigParser()
config.read('credentials.ini')


username_scihub  = config['COPERNICUS']['username_scihub'] 
password_scihub = config['COPERNICUS']['password_scihub'] 

# connect to the API
api = SentinelAPI(username_scihub, password_scihub, 'https://apihub.copernicus.eu/apihub')

#########################################################################################################################
# Function which retrieves a frame with all available sentinel 1 products ###############################################

def sentinel1(footprint, start_date_v2, end_date_v2):
    
    name, sensing_month, sensing_day, sensing_year, uuid, orbitdirection, relativeorbit  = ([] for i in range(7))
    
    sentinel_1_products = api.query(footprint,
                       date = (start_date_v2, end_date_v2),
                       platformname = 'Sentinel-1', 
                       producttype='GRD', 
                       relativeOrbitNumber=(160,167))
    
    print('Sentinel 1 Products\n')
    
    for product in list(sentinel_1_products):
        orbitdirection.append(sentinel_1_products[product]['orbitdirection'])
        name.append(sentinel_1_products[product]['title'])
        uuid.append(sentinel_1_products[product]['uuid'])
        relativeorbit.append(sentinel_1_products[product]['relativeorbitnumber'])
        try:
            sensing_m = int(datetime.datetime.strptime(sentinel_1_products[product]['summary'].split(",")[0][6:16], "%Y-%m-%d").month)
            sensing_d = int(datetime.datetime.strptime(sentinel_1_products[product]['summary'].split(",")[0][6:16], "%Y-%m-%d").day)
            sensing_y = int(datetime.datetime.strptime(sentinel_1_products[product]['summary'].split(",")[0][6:16], "%Y-%m-%d").year)
        except:
            sensing_m = int(sentinel_1_products[product]['beginposition'].month)
            sensing_d = int(sentinel_1_products[product]['beginposition'].day)
            sensing_y = int(sentinel_1_products[product]['beginposition'].year)
           
        sensing_month.append(sensing_m)
        sensing_day.append(sensing_d)
        sensing_year.append(sensing_y)
        
        
    print(f"The total number of found products: {len(list(sentinel_1_products))}")
    df_s1_read = pd.DataFrame({'Name': name, 'Sensing_month': sensing_month, 'Sensing_Day': sensing_day, 'Sensing_year': sensing_year, 'uuid': uuid, 'orbitdirection': orbitdirection, 'Orbit' : relativeorbit})
    print('\n')
    
    return df_s1_read


#####################################################################################################################
# Function which retrieves a frame with all available sensintel 2 products  #########################################

def sentinel2(footprint, start_date_v2, end_date_v2):
    
    name, sensing_month, sensing_day, sensing_year, cloudcoverpercentage, uuid = ([] for i in range(6))
    
    sentinel_2_products = api.query(footprint,
                       date = (start_date_v2, end_date_v2),
                       platformname = 'Sentinel-2',
                       processinglevel = 'Level-1C',
                       cloudcoverpercentage = (0, 15))
    
    print('Sentinel 2 Products\n')
    
    for product in list(sentinel_2_products):
        
        uuid.append(sentinel_2_products[product]['uuid'])
        name.append(sentinel_2_products[product]['title'])
        cloudcoverpercentage.append(sentinel_2_products[product]['cloudcoverpercentage'])           
        try:
            sensing_month.append(sentinel_2_products[product]['generationdate'].month)
            sensing_day.append(sentinel_2_products[product]['generationdate'].day)
            sensing_year.append(sentinel_2_products[product]['generationdate'].year)
        except:
            sensing_month.append(sentinel_2_products[product]['beginposition'].month)
            sensing_day.append(sentinel_2_products[product]['beginposition'].day)
            sensing_year.append(sentinel_2_products[product]['beginposition'].year)
        
        
        
    df_s2_read = pd.DataFrame({'Name': name, 'Sensing_month': sensing_month, 'Sensing_day': sensing_day, 'Sensing_year': sensing_year, 'Cloud_Cover': cloudcoverpercentage, 'uuid': uuid})
    print(f"The total number of found products: {len(list(sentinel_2_products))}")
    print('\n')
    
    return df_s2_read
 


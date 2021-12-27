'''
    Functions related to data accessing, such as saving and reading predict models, necessary csv files
'''

import streamlit as st
import os
import numpy as np
import pandas as pd
import gc
import math
import random
from datetime import datetime

# To load full data files into system memory. 
# To use Crime_data and df, you need to global Crime_data, df
Crime_data, df = None, None
def load_fullData():
    global Crime_data, df
    
    # Reading and processing data
    ## Getting crime_data
    print("Loading datafiles...", end="")
    Crime_2005_to_2007 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2005_to_2007.csv", error_bad_lines=False)
    Crime_2008_to_2011 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2008_to_2011.csv", error_bad_lines=False)
    Crime_2012_to_2017 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2012_to_2017.csv", error_bad_lines=False)
    print("Done!")
    ## Combining crime_data
    print("Combining crime_data...", end="")
    Crime_data = pd.concat([Crime_2005_to_2007, Crime_2008_to_2011, Crime_2012_to_2017])
    del Crime_2005_to_2007
    del Crime_2008_to_2011
    del Crime_2012_to_2017
    gc.collect()
    print("Done!")
    ## Processing and handling
    print("Dropping duplicated ones...", end="")
    Crime_data.drop_duplicates(subset=['Case Number'], inplace=True)
    print("Done!")
    print("Deleting unnecessary rows and columns...", end="")
    Crime_data.index = Crime_data['Case Number']    
    Crime_data.drop(Crime_data[ 
                    (Crime_data['Primary Type'] != "THEFT") &
                    (Crime_data['Primary Type'] != "MOTOR VEHICLE THEFT") &
                    (Crime_data['Primary Type'] != 'BURGLARY')
                ].index, inplace=True, axis=0)
    Crime_data.drop(['IUCR', 'ID', 'Description', 'Arrest', 'Domestic', 'Beat', 'FBI Code', 'Updated On'], inplace=True, axis=1)
    print("Done!")
    print("Handling NaN, null, None, 0, etc...", end="")
    Crime_data[['X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude']] = Crime_data[['X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude']].replace(0, np.NaN)
    Crime_data.dropna(inplace=True)
    print("Done!")
    print("Handling formats...", end="")
    Crime_data.Date = pd.to_datetime(Crime_data.Date, format="%m/%d/%Y %I:%M:%S %p")
    Crime_data.Latitude = Crime_data.Latitude.astype(float)
    df = pd.DataFrame(Crime_data)
    print("Done!")
    print("Deleting 2017...", end="")
    theBeginningOf2017 = datetime(2017, 1, 1)
    Crime_data.drop(df[df['Date'] >= theBeginningOf2017].index, inplace=True, axis=0)
    print("Done!")
    df = pd.DataFrame(Crime_data)
    gc.collect()
    print(Crime_data.info())
    
    
    
   
# Don't forget to close_data when no longer in use
def close_fullData():
    global Crime_data, df
    del Crime_data, df

## Data File Related
DataPath = "../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/"
DataFileName = [ 
    'Chicago_Crimes_2005_to_2007.csv', 
    'Chicago_Crimes_2008_to_2011.csv', 
    'Chicago_Crimes_2012_to_2017.csv'
]

def check_dataFiles():
    FileExist = True
    if os.path.exists(DataPath):
        for i in DataFileName:
            fullDataFileName = DataPath + i
            if os.path.exists(fullDataFileName) == False:
                FileExist = False
                break
    return FileExist


## Comoonly used DataFrame Related
def check_DataFrames():
    return False

def create_DataFrames():    
    global Crime_data, df
    
    # Getting needed dataframes
    ## Crime count by primary types in each hour
    CrimeCountByHour = pd.crosstab(Crime_data['Date'].dt.floor('h'), Crime_data['Primary Type'])
        # You can easily get by day and by year, so it won't be necessary to save them
    ## Crime count by Location Description in each year
    CrimeCountByYearByLocationDescription = pd.crosstab(Crime_data['Date'].dt.to_period('Y'), Crime_data['Location Description'])
    ## District
    DistrictToCoordinates_max = (df[['District', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['District']).max()
    DistrictToCoordinates_min = (df[['District', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['District']).min()
    DistrictToCoordinates_mean = (df[['District', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['District']).mean()
    CrimeCountByDistrict = pd.crosstab(Crime_data['District'], Crime_data['Primary Type']) # All Data in Total
    ## Streets
    streetNames = []
    for i in Crime_data['Block']:
            streetName = i.split(' ', 2)[2]
            streetNames.append(streetName)
    newPd = df.copy()
    newPd['Street'] = streetNames    
    CrimeCountByStreet = pd.crosstab(newPd['Street'], Crime_data['Primary Type'])
    StreetNameToCoordinates_max = (newPd[['Street', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Street']).max()
    StreetNameToCoordinates_min = (newPd[['Street', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Street']).min()
    StreetNameToCoordinates_mean = (newPd[['Street', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Street']).mean()
    ## Block
    
    
    
    
    
    # Saving needed dataframes
    
    
    del df, Crime_data # To close the file
    return check_DataFrames()


## Prediction Model Related
def check_models():
    return False

# You must create dataframes before creating models
def create_models():
    if check_DataFrames() == False:
        return False
    return check_models()
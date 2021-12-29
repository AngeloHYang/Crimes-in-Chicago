'''
    Functions related to data accessing, such as saving and reading predict models, necessary csv files
'''

import streamlit as st
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gc
import math
import random
import time
from datetime import datetime
import util

# To load full data files into system memory. 
# To use Crime_data and df, you need to global Crime_data, df
Crime_data, df = None, None
def load_fullData():
    print("\nLoading full file data:")
    global Crime_data, df
    
    # This to make sure that data file will be read only once
    if 'DataFilesLoaded' not in st.session_state or st.session_state['DataFilesLoaded'] == False:
        Crime_data = None
        df = None
        startTime = time.time()
        
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
        endTime = time.time()
        print("Loading full file data done! Took:", time.strftime("%H:%M:%S", time.gmtime(endTime - startTime)) , "\n")
        
        st.session_state['DataFilesLoaded'] = True
    else:
        print("Already loaded!\n")


# Don't forget to close_data when no longer in use
def close_fullData():
    global Crime_data, df
    print("Releasing full data memory usage...", end="")
    del st.session_state['DataFilesLoaded']
    Crime_data = None
    df = None
    print("Done!")

## Data File Related
DataPath = "../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/"
DataFileName = [ 
    'Chicago_Crimes_2005_to_2007.csv', 
    'Chicago_Crimes_2008_to_2011.csv', 
    'Chicago_Crimes_2012_to_2017.csv'
]

def check_dataFiles():
    return util.checkFiles(DataPath, DataFileName)



## Comoonly used DataFrame Related
DataFramePath = "./DataFrames/"
#You'll need to add .csv when accessing in data
DataFrames = [
    "CrimeCountByHour", 
    "CrimeCountByYearByLocationDescription", 
    "CrimeCountByLocationDescription", 
    "DistrictToCoordinates_max", 
    "DistrictToCoordinates_min", 
    "DistrictToCoordinates_mean",     
    "CrimeCountByDistrict", 
    "CrimeCountByStreet", 
    "StreetNameToCoordinates_max", 
    "StreetNameToCoordinates_min", 
    "StreetNameToCoordinates_mean", 
    "CrimeCountByBlock", 
    "BlockNameToCoordinates_max", 
    "BlockNameToCoordinates_min", 
    "BlockNameToCoordinates_mean", 
    "CrimeCountByWard", 
    "WardToCoordinates_max", 
    "WardToCoordinates_min", 
    "WardToCoordinates_mean", 
    "CrimeCountByCommunityArea", 
    "CommunityAreaToCoordinates_max", 
    "CommunityAreaToCoordinates_min", 
    "CommunityAreaToCoordinates_mean"]
def check_dataFrames():
    return util.checkFiles(DataFramePath, DataFrames, fileNameExtension=".csv")

def create_dataFrames():    
    global Crime_data, df
    startTime = time.time()

    print("\nCreating DataFrames:")
    
    # Getting needed dataframes
    print("Generating dataframes in memory...", end="")
    ## Crime count by primary types in each hour
    CrimeCountByHour = pd.crosstab(Crime_data['Date'].dt.floor('h'), Crime_data['Primary Type'])
        # You can easily get by day and by year, so it won't be necessary to save them
    ## Crime count by Location Description in each year
    CrimeCountByYearByLocationDescription = pd.crosstab(Crime_data['Date'].dt.to_period('Y'), Crime_data['Location Description'])
    ## Crime count by primary types by Location Description
    CrimeCountByLocationDescription = pd.crosstab(Crime_data['Location Description'], Crime_data['Primary Type'])
    
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
    CrimeCountByBlock = pd.crosstab(Crime_data['Block'], Crime_data['Primary Type'])
    BlockNameToCoordinates_max = (df[['Block', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Block']).max()
    BlockNameToCoordinates_min = (df[['Block', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Block']).min()
    BlockNameToCoordinates_mean = (df[['Block', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Block']).mean()
    ## Ward
    CrimeCountByWard = pd.crosstab(Crime_data['Ward'], Crime_data['Primary Type'])
    WardToCoordinates_max = (df[['Ward', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Ward']).max()
    WardToCoordinates_min = (df[['Ward', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Ward']).min()
    WardToCoordinates_mean = (df[['Ward', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Ward']).mean()
    ## Community Area
    CrimeCountByCommunityArea = pd.crosstab(Crime_data['Community Area'], Crime_data['Primary Type'])
    CommunityAreaToCoordinates_max = (df[['Community Area', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Community Area']).max()
    CommunityAreaToCoordinates_min = (df[['Community Area', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Community Area']).min()
    CommunityAreaToCoordinates_mean = (df[['Community Area', 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby(['Community Area']).mean()
    print("Done!")
    
    # Saving needed dataframes
    dataHandlingEndTime = time.time()
    
    print("Saving DataFrames readme file...", end="")
    if not os.path.exists(DataFramePath):
        os.makedirs(DataFramePath)
    
    CrimeCountByHour.to_csv(DataFramePath + "CrimeCountByHour.csv")
    CrimeCountByYearByLocationDescription.to_csv(DataFramePath + "CrimeCountByYearByLocationDescription.csv")
    CrimeCountByLocationDescription.to_csv(DataFramePath + "CrimeCountByLocationDescription.csv")
    DistrictToCoordinates_max.to_csv(DataFramePath + "DistrictToCoordinates_max.csv")
    DistrictToCoordinates_min.to_csv(DataFramePath + "DistrictToCoordinates_min.csv")
    DistrictToCoordinates_mean.to_csv(DataFramePath + "DistrictToCoordinates_mean.csv")
    CrimeCountByDistrict.to_csv(DataFramePath + "CrimeCountByDistrict.csv")
    CrimeCountByStreet.to_csv(DataFramePath + "CrimeCountByStreet.csv")
    StreetNameToCoordinates_max.to_csv(DataFramePath + "StreetNameToCoordinates_max.csv")
    StreetNameToCoordinates_min.to_csv(DataFramePath + "StreetNameToCoordinates_min.csv")
    StreetNameToCoordinates_mean.to_csv(DataFramePath + "StreetNameToCoordinates_mean.csv")
    CrimeCountByBlock.to_csv(DataFramePath + "CrimeCountByBlock.csv")
    BlockNameToCoordinates_max.to_csv(DataFramePath + "BlockNameToCoordinates_max.csv")
    BlockNameToCoordinates_min.to_csv(DataFramePath + "BlockNameToCoordinates_min.csv")
    BlockNameToCoordinates_mean.to_csv(DataFramePath + "BlockNameToCoordinates_mean.csv")
    CrimeCountByWard.to_csv(DataFramePath + "CrimeCountByWard.csv")
    WardToCoordinates_max.to_csv(DataFramePath + "WardToCoordinates_max.csv")
    WardToCoordinates_min.to_csv(DataFramePath + "WardToCoordinates_min.csv")
    WardToCoordinates_mean.to_csv(DataFramePath + "WardToCoordinates_mean.csv")
    CrimeCountByCommunityArea.to_csv(DataFramePath + "CrimeCountByCommunityArea.csv")
    CommunityAreaToCoordinates_max.to_csv(DataFramePath + "CommunityAreaToCoordinates_max.csv")
    CommunityAreaToCoordinates_min.to_csv(DataFramePath + "CommunityAreaToCoordinates_min.csv")
    CommunityAreaToCoordinates_mean.to_csv(DataFramePath + "CommunityAreaToCoordinates_mean.csv")
    print("Done!")
    
    savingEndTime = time.time()
    print("Generating DataFrames readme file...", end="")
    readmeFile = open(DataFramePath + "README.txt",'w')
    readmeFile.write("Creation Start Time:" + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(startTime)) + "\n")
    readmeFile.write("Creation End Time:" + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(dataHandlingEndTime)) + "\n")
    readmeFile.write("Saving Time:" + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(savingEndTime)) + "\n")
    readmeFile.write("Time spent on generating: " + time.strftime("%H:%M:%S", time.gmtime(dataHandlingEndTime - startTime)) + "\n")
    readmeFile.write("Time spent on saving: " + time.strftime("%H:%M:%S", time.gmtime(savingEndTime - dataHandlingEndTime)) + "\n")
    print("Done!")
    
    readmeFile.close()
    
    return check_dataFrames()

# To load comonly used dataFrames into the session
def load_dataFrames():
    if 'dataFramesLoaded' in st.session_state and st.session_state['dataFramesLoaded'] == True:
        return True
    elif check_dataFrames() == False:
        return False
    else:
        st.session_state['dataFrames'] = dict()
        for i in DataFrames:
            fileName = DataFramePath +  i + '.csv'
            theFile = pd.read_csv(fileName)
            st.session_state['dataFrames'].append({i: theFile})
        st.session_state['dataFramesLoaded'] = True
        return True
    
#to clear memory used by loaded dataframs
def close_dataFrames():
    util.batch_delele_from_sessionState('dataFrames')

## Prepared graphs
PreparedGraphPath = "./PreparedGraphs/"
Graphs = []
def check_preparedGraphs():
    return False

# Only time counsuming or full data required graphs will be prepared
def create_preparedGraphs():
    
    # To Paint the Map it's better to work with all datas
    Crime_data = None
    df = None
    startTime = time.time()
    
    # Reading and processing data
    ## Getting crime_data
    print("Loading datafiles for painting...", end="")
    Crime_2001_to_2004 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2001_to_2004.csv", error_bad_lines=False)
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
    Crime_data.drop(['ID', 'Date', 'IUCR',
       'Primary Type', 'Description', 'Location Description', 'Arrest',
       'Domestic', 'Beat', 'FBI Code',
       'Year', 'Updated On'], inplace=True, axis=1)
    print("Done!")
    print("Handling NaN, null, None, 0, etc...", end="")
    Crime_data[['X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude']] = Crime_data[['X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude']].replace(0, np.NaN)
    Crime_data.dropna(inplace=True)
    print("Done!")
    print("Handling formats...", end="")
    Crime_data.Latitude = Crime_data.Latitude.astype(float)
    df = pd.DataFrame(Crime_data)
    print("Done!")
    gc.collect()

    print(Crime_data.info())
    endTime = time.time()
    print("Loading painting file data done! Took:", time.strftime("%H:%M:%S", time.gmtime(endTime - startTime)) , "\n")
    
    # Creating Folder
    if not os.path.exists(PreparedGraphPath):
        os.makedirs(PreparedGraphPath)
    
    # README file
    print("Generating PreparedGraph readme file...", end="")
    readmeFile = open(PreparedGraphPath + "README.txt",'w')
    print("Done!")
    totalStartTime = time.time()
    readmeFile.write("Total Start Time:" + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(startTime)) + "\n")
    
    # Paint with District
    util.createAndSaveMap("District", readmeFile, Crime_data, df, PreparedGraphPath)
    
    # Paint with Ward
    util.createAndSaveMap("Ward", readmeFile, Crime_data, df, PreparedGraphPath)
    
    # Paint with Community Area
    util.createAndSaveMap("Community Area", readmeFile, Crime_data, df, PreparedGraphPath)
    
    print("")
    Crime_data = None
    df = None
    plt.close('all')   
    #plt.close(fig)
    readmeFile.close()
    gc.collect()
    return False

## Prediction Model Related
def check_models():
    return False

# You must create dataframes before creating models
def create_models():
    if check_dataFrames() == False:
        return False
    return check_models()
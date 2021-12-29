'''
    Utilities that may come handy, the ones that'll be called constantly
'''
import streamlit as st
import os
import time
import matplotlib.pyplot as plt
import pandas as pd

from fbprophet import Prophet
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
from fbprophet.plot import plot_cross_validation_metric, add_changepoints_to_plot, plot_plotly
import json
from fbprophet.serialize import model_to_json, model_from_json

# When you want to delete a bunch of keys from 
def batch_delele_from_sessionState(stringOrList):
    if isinstance(stringOrList, str):
        if stringOrList in st.session_state:
            del st.session_state[stringOrList]
    elif isinstance(stringOrList, list):
        for i in stringOrList:
            if i in st.session_state:
                del st.session_state[i]
    else:
        print('Delete from session_state error')
        
def checkFiles(pathString, fileNameList, fileNameExtension=""):
    if not os.path.exists(pathString) or not os.path.isdir(pathString):
        return False
        
    Exist = True
    for i in fileNameList:
        filename = i + fileNameExtension
        if not os.path.exists(pathString + filename) or not os.path.isfile(pathString + filename):
            Exist = False
            break
    return Exist
    
    
def create_dataframe_countByPlace_and_coordinate_max_min_mean(PlaceName, Crime_data):
    CrimeCountByPlace = pd.crosstab(Crime_data[PlaceName], Crime_data['Primary Type'])
    PlaceToCoordinates_max = (Crime_data[[PlaceName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby([PlaceName]).max()
    PlaceToCoordinates_min = (Crime_data[[PlaceName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby([PlaceName]).min()
    PlaceToCoordinates_mean = (Crime_data[[PlaceName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby([PlaceName]).mean()
    return CrimeCountByPlace, PlaceToCoordinates_max, PlaceToCoordinates_min, PlaceToCoordinates_mean
    

def createAndSaveMap(MapName, readmeFile, Crime_data, PreparedGraphPath):
    print("Painting ", MapName, " map...", end="", sep="")
    startTime = time.time()
    readmeFile.write("\n" + MapName + "Map:\n")
    readmeFile.write("Start Time:" + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(startTime)) + "\n")
    ## Get necessary lists
    MapElements = list((Crime_data.drop(['Case Number'], axis=1).reset_index())[MapName].drop_duplicates())
    MapElementToCoordinates_mean_dict = (Crime_data[[MapName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby([MapName]).mean().to_dict()
    MapElementDf = Crime_data[[MapName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)
    ## Calculate points
    thePointUsedForMapElementLabelDict = dict()
    for MapElement in MapElements:
        theElement = MapElementDf[MapElementDf[MapName] == MapElement]
        LatDistance = theElement['Latitude'].sub(MapElementToCoordinates_mean_dict['Latitude'][MapElement]).abs()
        LonDistance = theElement['Longitude'].sub(MapElementToCoordinates_mean_dict['Longitude'][MapElement]).abs()
        totalDistance = LatDistance.mul(LatDistance) + LonDistance.mul(LonDistance)
        theID = totalDistance.sort_values(ascending=True).index[0]
        thePointUsedForMapElementLabelDict[MapElement] = theID
    ## Paint it
    plt.figure(figsize=(10, 10), dpi=250)
    cm = plt.cm.get_cmap('Spectral')
    plt.scatter(x=Crime_data['X Coordinate'], y=Crime_data['Y Coordinate'], c=Crime_data[MapName], s=1, cmap=cm)
    for MapElement in MapElements:
        plt.text(
            x=Crime_data['X Coordinate'][thePointUsedForMapElementLabelDict[MapElement]], 
            y=Crime_data['Y Coordinate'][thePointUsedForMapElementLabelDict[MapElement]],
            s= int(MapElement)
        )        
    plt.savefig(PreparedGraphPath + MapName + " Map")
    print("Done!")
    endTime = time.time()
    readmeFile.write("End Time:" + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(endTime)) + "\n")
    readmeFile.write("Took: " + time.strftime("%H:%M:%S", time.gmtime(endTime - startTime)) + "\n")
    print("Took: " + time.strftime("%H:%M:%S", time.gmtime(endTime - startTime)), "to generate", MapName)
    
def createProphetModel(neededDf, timeType, selectingCondition = [True]*len(neededDf)):
    #selectingCondition = (neededDf['Primary Type'] == 'BURGLARY') & (neededDf['Location Description'] == 'STREET')
    theDf = neededDf[selectingCondition]
    
    theDataset = theDf.groupby(theDf['Date'].dt.to_period(timeType)).count()['Block']
    theDataset = pd.DataFrame(theDataset).reset_index().rename(columns={"Date": "ds", "Block": "y"})
    theDataset['ds'] = pd.to_datetime(theDataset['ds'].dt.to_timestamp('s'), format="%m/%d/%Y %I:%M:%S")
    
    LocationDiscription_crosstab = pd.crosstab(theDf['Date'].dt.to_period(timeType), theDf['Location Description']).reset_index().rename(columns={"Date": "ds"})
    LocationDiscription_crosstab['ds'] = pd.to_datetime(LocationDiscription_crosstab['ds'].dt.to_timestamp('s'), format="%m/%d/%Y %I:%M:%S")
    theDataset = pd.merge(theDataset, LocationDiscription_crosstab, how='outer', on='ds').replace(np.nan, 0)
    
    # Config Prophet
    prophet = Prophet(
        growth='linear',
        seasonality_mode = 'additive'
    )
    if timeType.upper() == 'H':
        prophet.daily_seasonality = True
        prophet.weekly_seasonality = True
        prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        prophet.yearly_seasonality = True
    if timeType.upper() == 'D':
        prophet.daily_seasonality = True
        prophet.weekly_seasonality = True
        prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        prophet.yearly_seasonality = True
    if timeType.upper() == 'M':
        prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        prophet.yearly_seasonality = True
    if timeType.upper() == 'Y':
        prophet.yearly_seasonality = True   
    prophet.add_country_holidays(country_name='US')
    for i in LocationDiscriptionName:
        prophet.add_regressor(i)
    
    # Run it
    prophet.fit(theDataset)
    
    return prophet
'''
    Utilities that may come handy, the ones that'll be called constantly
'''
import streamlit as st
import os
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

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
    
    
def create_dataframe_coordinate_max_min_mean_closest_most(PlaceName, Crime_data):
    PlaceToCoordinates_max = (Crime_data[[PlaceName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby([PlaceName]).max()
    PlaceToCoordinates_min = (Crime_data[[PlaceName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby([PlaceName]).min()
    PlaceToCoordinates_mean = (Crime_data[[PlaceName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby([PlaceName]).mean()
    PlaceToCoordinates_closest = (Crime_data[[PlaceName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1))
    PlaceToCoordinates_closest[['Lat', 'Lon']] = (Crime_data[['Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1))
    PlaceToCoordinates_closest['Lat'] = PlaceToCoordinates_closest['Lat'].sub(PlaceToCoordinates_closest['Latitude'].mean())
    PlaceToCoordinates_closest['Lon'] = PlaceToCoordinates_closest['Lon'].sub(PlaceToCoordinates_closest['Longitude'].mean())
    PlaceToCoordinates_closest['Dist'] = PlaceToCoordinates_closest['Lat'].mul(PlaceToCoordinates_closest['Lat']).add(PlaceToCoordinates_closest['Lon'].mul(PlaceToCoordinates_closest['Lon']))
    PlaceToCoordinates_closest = PlaceToCoordinates_closest.groupby([PlaceName]).min().drop(['Lat', 'Lon', 'Dist'], axis=1)
    
    # Mode
    ## Read
    PlaceToCoordinates_most = (Crime_data[[PlaceName, 'Location']].reset_index().drop(['Case Number'], axis=1))
    ## Find
    PlaceToCoordinates_most = PlaceToCoordinates_most.groupby([PlaceName]).agg(lambda x: x.value_counts().index[0])
    ## split and combine
    PlaceToCoordinates_most = PlaceToCoordinates_most['Location'].str.split(",", n = 2, expand = True)
    PlaceToCoordinates_most[0] = PlaceToCoordinates_most[0].str.lstrip('(')
    PlaceToCoordinates_most[1] = PlaceToCoordinates_most[1].str.rstrip(')')
    PlaceToCoordinates_most.rename(columns={0: 'Latitude', 1: "Longitude"}, inplace=True)
    PlaceToCoordinates_most.Latitude = PlaceToCoordinates_most.Latitude.astype(float)
    PlaceToCoordinates_most.Longitude = PlaceToCoordinates_most.Longitude.astype(float)
    
    return PlaceToCoordinates_max, PlaceToCoordinates_min, PlaceToCoordinates_mean, PlaceToCoordinates_closest, PlaceToCoordinates_most
    

def createAndSaveMap(MapName, readmeFile, Crime_data, PreparedGraphPath):
    print("Painting ", MapName, " map...", end="", sep="")
    readmeFile.write(MapName + " Map")
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
    readmeFile.write(MapName + " Map", isStartTime=False)

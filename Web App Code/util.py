'''
    Utilities that may come handy
'''
import streamlit as st
import os
import time
import matplotlib.pyplot as plt

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

def createAndSaveMap(MapName, readmeFile, Crime_data, df, PreparedGraphPath):
    print("Painting ", MapName, " map...", end="", sep="")
    startTime = time.time()
    readmeFile.write("\n" + MapName + "Map:\n")
    readmeFile.write("Start Time:" + time.strftime('%Y-%m-%d %H:%M:%S %z' , time.localtime(startTime)) + "\n")
    ## Get necessary lists
    MapElements = list((Crime_data.drop(['Case Number'], axis=1).reset_index())[MapName].drop_duplicates())
    MapElementToCoordinates_mean_dict = (df[[MapName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)).groupby([MapName]).mean().to_dict()
    MapElementDf = df[[MapName, 'Latitude', 'Longitude']].reset_index().drop(['Case Number'], axis=1)
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
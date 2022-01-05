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

# evaluation related
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score

# fbprophet related
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
    
    # timeType can be H, D, W, M, Y
def createProphetModel(neededDf, timeType, selectingCondition, Crime_data_2003_to_2004, selectAll = True):
    #selectingCondition = (neededDf['Primary Type'] == 'BURGLARY') & (neededDf['Location Description'] == 'STREET')
    # Apply data selecting to neededDf
    if selectAll:
        theDf = neededDf[[True]*len(neededDf)]
    else:
        theDf = neededDf[selectingCondition]
    theDataset = theDf.groupby(theDf['Date'].dt.to_period(timeType)).count()['Block']
    theDataset = pd.DataFrame(theDataset).reset_index().rename(columns={"Date": "ds", "Block": "y"})
    theDataset['ds'] = pd.to_datetime(theDataset['ds'].dt.to_timestamp('s'), format="%m/%d/%Y %I:%M:%S")
    
    # Apply data selecting to Crime_data_2003_to_2004
    if selectAll:
        theRestDf = Crime_data_2003_to_2004[[True]*len(Crime_data_2003_to_2004)]
    else:
        theRestDf = Crime_data_2003_to_2004[selectingCondition]
    theDataset_2003_to_2004 = theRestDf.groupby(theRestDf['Date'].dt.to_period(timeType)).count()['Block']
    theDataset_2003_to_2004 = pd.DataFrame(theDataset_2003_to_2004).reset_index().rename(columns={"Date": "ds", "Block": "y"})
    theDataset_2003_to_2004['ds'] = pd.to_datetime(theDataset_2003_to_2004['ds'].dt.to_timestamp('s'), format="%m/%d/%Y %I:%M:%S")
    
    # Added Location info to theDataset
    # LocationDiscriptionName = list(theDf['Location Description'].drop_duplicates())
    # LocationDiscription_crosstab = pd.crosstab(theDf['Date'].dt.to_period(timeType), theDf['Location Description']).reset_index().rename(columns={"Date": "ds"})
    # LocationDiscription_crosstab['ds'] = pd.to_datetime(LocationDiscription_crosstab['ds'].dt.to_timestamp('s'), format="%m/%d/%Y %I:%M:%S")
    # theDataset = pd.merge(theDataset, LocationDiscription_crosstab, how='outer', on='ds').replace(np.nan, 0)
    
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
    # for i in LocationDiscriptionName:
    #     prophet.add_regressor(i)
    
    # Run it
    prophet.fit(theDataset)
    
    return prophet, theDataset_2003_to_2004

def generateModelName(timeType, crimeType, locationType):
    # timeType can be H, D, W, M, Y
    # crimeType can be ALL, BURGLARY, MOTOR VEHICLE THEFT, THEFT
    # LocationType can be All, Community Area, District, Street, Block, Ward
    FileName = ''
    
    # deal with timeType
    if timeType == 'H':
        FileName += 'ByHour'
    elif timeType == 'D':
        FileName += 'ByDay'
    elif timeType == 'W':
        FileName += 'ByWeek'
    elif timeType == 'M':
        FileName += 'ByMonth'
    elif timeType == 'Y':
        FileName += 'ByYear'
    else:
        return False
    
    # deal with crimeType
    if crimeType == 'ALL':
        FileName += "AllCrime"
    elif crimeType == 'BURGLARY':
        FileName += 'Burglary'
    elif crimeType == 'MOTOR VEHICLE THEFT':
        FileName += 'MotorVehicleTheft'
    elif crimeType == 'THEFT':
        FileName += 'Theft'
    else:
        return False
    
    # deal with LocationType
    if locationType == 'All':
        FileName += 'WholeCity'
    elif locationType == 'Community Area':
        FileName += 'ByCommunityArea'
    elif locationType == 'District':
        FileName += 'ByDistrict'
    elif locationType == 'Street':
        FileName += 'ByStreet'
    elif locationType == 'Block':
        FileName += 'ByBlock'
    elif locationType == 'Ward':
        FileName += 'ByWard'
    else:
        return False
    return FileName        

def generateModelSelection(crimeType, locationType):
# Based on crimeType and locationType
# Get selectingCondition and selectAll value
# double False stands for error
    crimeSelection = "(neededDf['Primary Type'] == "
    locationSelection = "(neededDf['Location Description'] == "
    
    # deal with crimeType
    if crimeType == 'ALL':
        crimeSelection = ""
    elif crimeType == 'BURGLARY':
        crimeSelection += "'BURGLARY')"
    elif crimeType == 'MOTOR VEHICLE THEFT':
        crimeSelection += "'MOTOR VEHICLE THEFT)'"
    elif crimeType == 'THEFT':
        crimeSelection += "'THEFT')"
    else:
        return False, False
    
    # deal with LocationType
    if locationType == 'All':
        locationSelection = ""
    elif locationType == 'Community Area':
        locationSelection += "'Community Area')"
    elif locationType == 'District':
        locationSelection += "'District')"
    elif locationType == 'Street':
        locationSelection += "'Street')"
    elif locationType == 'Block':
        locationSelection += "'Block')"
    elif locationType == 'Ward':
        locationSelection += "'Ward')"
    else:
        return False, False
    
    if not (crimeSelection or locationSelection):
        return None, True
    elif crimeSelection and locationSelection:
        return crimeSelection + " & " + locationSelection, False
    else:
        return crimeSelection + locationSelection, False
    

def saveProphetModel(ModelPath, model, modelName):
    #FileName = generateModelName(timeType, crimeType, locationType)
    FileName = modelName + '.json'
    if not FileName or not model:
        return False
    with open(ModelPath + FileName, 'w') as fout:
        json.dump(model_to_json(model), fout)  # Save model
        return True
    return False
    
def evaluateModel(model, restDataframe, readmeFile, model_name):
    y_true = restDataframe
    y_predicted = pd.DataFrame(restDataframe['ds'])
    y_predicted = model.predict(y_predicted)
    
    y_true = y_true['y'].values
    y_predicted = y_predicted['yhat'].values
    
    # print('MAE: %.3f' % mean_absolute_error(y_true, y_predicted))
    # print('MSE: %.3f' % mean_squared_error(y_true, y_predicted))
    # print('RMSE: %.3f' % math.sqrt(mean_squared_error(y_true, y_predicted)))
    # print('Explained variance: %.3f' % explained_variance_score(y_true, y_predicted))
    # print('Coefficient of determination: %.3f' % r2_score(y_true, y_predicted))
    readmeFile.writeEvaluation(model_name, "MAE", mean_absolute_error(y_true, y_predicted))
    readmeFile.writeEvaluation(model_name, "MSE", mean_squared_error(y_true, y_predicted))
    readmeFile.writeEvaluation(model_name, "RMSE", math.sqrt(mean_squared_error(y_true, y_predicted)))
    readmeFile.writeEvaluation(model_name, "Explained variance", explained_variance_score(y_true, y_predicted))
    readmeFile.writeEvaluation(model_name, "Coefficient of determination", r2_score(y_true, y_predicted))

def modelErrorDetect(Reason, timeType, crimeType, locationType):
    print(Reason, "timeType:", timeType, "crimeType:", crimeType, "locationType:", locationType)

# This is the method that does everything about model creation, the one you need to use
def handleTheModel(neededDf, Crime_data_2003_to_2004, ModelPath, readmeFile, timeType, crimeType, locationType):
    # get name
    model_name = generateModelName(timeType, crimeType, locationType)
    if not model_name:
        modelErrorDetect("model_name error!", timeType, crimeType, locationType)
        return False
    readmeFile.write(model_name)
    print("Creating...", model_name, end="")
    
    # get condition
    selectingCondition, selectAll = generateModelSelection(crimeType, locationType)
    if not (selectingCondition or selectAll):
        modelErrorDetect("Selecting Condition error!", timeType, crimeType, locationType)
        return False
    
    # Create model
    theModel, restDataframe = createProphetModel(neededDf, timeType, selectingCondition, Crime_data_2003_to_2004, selectAll)
    readmeFile.write(model_name, isStartTime=False)
    evaluateModel(theModel, restDataframe, readmeFile, model_name)
    if not saveProphetModel(ModelPath, theModel, model_name):
        modelErrorDetect("Save Model error!", timeType, crimeType, locationType)
        return False
    print("Done!")
    return True
    
'''
    This is the page about model training and data prediction
'''

import streamlit as st
import dateUtil
import datetime
from dataAccess import return_dataFrames
import pandas as pd
import themeUtil
import queryUtil
import modelUtil
import util
import numpy as np

import time

def modelEvaluations():
    # # Read it 
    mapType = st.session_state['predictPage']['mapType']
    crimeTypeSelects = st.session_state['predictPage']['crimeTypeSelects']
    if mapType != 'Whole City':
        mapElementSelects = st.session_state['predictPage']['mapElementSelects']
    # timeType = st.session_state['predictPage']['timeType']
    timePrecision = st.session_state['predictPage']['timePrecision']
    # startTime = st.session_state['predictPage']['startTime']
    # if timeType == 'A Period':
    #     endTime = st.session_state['predictPage']['endTime']
    
    # # init
    # # False for not exist or error
    # theSize = 1 if mapType == 'Whole City' else len(mapElementSelects)
    
    models = st.session_state['predictPage']['models']
    modelTimeSpend = st.session_state['predictPage']['modelTimeSpend']
    modelEvaluations = st.session_state['predictPage']['modelEvaluations']
    
    strings = []
    modelString = ""
    if mapType == 'Whole City':
        modelString = ""
        query = queryUtil.get_CrimeType_and_Location_query(crimeTypeSelects, mapType, [])
        modelString += 'Model: ' + query
        if models[0] == False:
            modelString += ": False"
            modelString += "  \n  "
            modelString += " Time precision: " + timePrecision
            modelString += "  \n  "
        else:
            modelString += ": True"
            modelString += "  \n  "
            modelString += " Time precision: " + timePrecision
            modelString += "  \n  "
            modelString += "Took: " + time.strftime("%H:%M:%S", time.gmtime(modelTimeSpend[0]))
            modelString += "  \n  "
            if modelEvaluations[0][1] == True:
                modelString += modelUtil.evaluateModel(models[0], modelEvaluations[0][0])
                modelString += "  \n  "
            else:
                modelString += "Evaluation: False  \n  "
        modelString += "  \n  "
        strings.append(modelString)
    else:
        for i in range(len(mapElementSelects)):
            modelString = ""
            query = queryUtil.get_CrimeType_and_Location_query(crimeTypeSelects, mapType, [mapElementSelects[i]])
            modelString += 'Model: ' + query
            if models[i] == False:
                modelString += ": False"
                modelString += "  \n  "
                modelString += " Time precision: " + timePrecision
                modelString += "  \n  "
            else:
                modelString += ": True"
                modelString += "  \n  "
                modelString += " Time precision: " + timePrecision
                modelString += "  \n  "
                modelString += "Took: " + time.strftime("%H:%M:%S", time.gmtime(modelTimeSpend[i]))
                modelString += "  \n  "
                if modelEvaluations[i][1] == True:
                    modelString += modelUtil.evaluateModel(models[i], modelEvaluations[i][0])
                    modelString += "  \n  "
                else:
                    modelString += "Evaluation: False  \n  "
            modelString += "  \n  "
            strings.append(modelString)
    
    
    string = ""
    for i in strings:
        string += i
    st.write(string)
    
            

def handleData():
    # Read it 
    mapType = st.session_state['predictPage']['mapType']
    crimeTypeSelects = st.session_state['predictPage']['crimeTypeSelects']
    if mapType != 'Whole City':
        mapElementSelects = st.session_state['predictPage']['mapElementSelects']
    timeType = st.session_state['predictPage']['timeType']
    timePrecision = st.session_state['predictPage']['timePrecision']
    startTime = st.session_state['predictPage']['startTime']
    if timeType == 'A Period':
        endTime = st.session_state['predictPage']['endTime']
    
    # init
    # False for not exist or error
    theSize = 1 if mapType == 'Whole City' else len(mapElementSelects)
    models = [False] * theSize
    modelTimeSpend = [False] * theSize
    modelEvaluations = [[False, False]] * theSize

    
    # Handle models and modelEvaluations
    if mapType == 'Whole City':
        models[0] = modelUtil.getModelToUse(timePrecision, crimeTypeSelects, mapType, [])
        if models[0] != False:
            modelTimeSpend[0] = time.time()
            modelEvaluations[0][0], modelEvaluations[0][1] = modelUtil.getEvaluationModelToUse(timePrecision, crimeTypeSelects, mapType, [])
            modelTimeSpend[0] = time.time() - modelTimeSpend[0]
        else:
            modelTimeSpend[0] = 0
            modelEvaluations[0][0], modelEvaluations[0][1] = False, False
    else:
        for i in range(len(mapElementSelects)):
            modelTimeSpend[i] = time.time()
            models[i] = modelUtil.getModelToUse(timePrecision, crimeTypeSelects, mapType, [mapElementSelects[i]])
            modelTimeSpend[i] = time.time() - modelTimeSpend[i]
            if models[i] != False:
                modelEvaluations[i][0], modelEvaluations[i][1] = modelUtil.getEvaluationModelToUse(timePrecision, crimeTypeSelects, mapType, [])
            else:
                modelEvaluations[i][0], modelEvaluations[i][1] = False, False
        
    
        
    if timeType == 'A Moment':
        dataframe = pd.DataFrame(columns=([mapType, 'Count']))
        if mapType == 'Whole City':
            if models[0] != False:
                dataframe = dataframe.append(
                    {
                        'Count': modelUtil.predictMoment(models[0], startTime),
                        mapType: 'Whole City'
                    },
                    ignore_index=True
                )
        else:
            for i in range(len(mapElementSelects)):
                if models[i] != False:
                    dataframe = dataframe.append(
                        {
                            'Count': modelUtil.predictMoment(models[i], startTime),
                            mapType: mapElementSelects[i]
                        },
                        ignore_index=True
                    )
    else:
        dataframe = pd.DataFrame(columns=(["Date", mapType, 'Count']))
        if mapType == 'Whole City' and models[0] != False:
            dataframeOfTheElement = modelUtil.predictPeriod(models[0], startTime, endTime, timePrecision)
            dataframeOfTheElement.rename(columns={"ds": "Date", "yhat": "Count"}, inplace=True)
            dataframeOfTheElement[mapType] = 'Whole City'
            dataframe = dataframe.append(dataframeOfTheElement, ignore_index=True)
        else:
            for i in range(len(mapElementSelects)):
                if models[i] != False:
                    dataframeOfTheElement = modelUtil.predictPeriod(models[i], startTime, endTime, timePrecision)
                    dataframeOfTheElement.rename(columns={"ds": "Date", "yhat": "Count"}, inplace=True)
                    dataframeOfTheElement[mapType] = mapElementSelects[i]
                    dataframe = dataframe.append(dataframeOfTheElement, ignore_index=True)
    
    st.session_state['predictPage']['models'] = models
    st.session_state['predictPage']['modelTimeSpend'] = modelTimeSpend
    st.session_state['predictPage']['modelEvaluations'] = modelEvaluations
    st.session_state['predictPage']['dataframe'] = dataframe

def timeError():
    st.error("Time Error!  \n  Please check your start time and your end time")

def preparedMapResult():
    filenameList = [st.session_state['predictPage']['mapType'] + " Map"]
    if util.checkFiles(
            './PreparedGraphs/',
            filenameList,
            fileNameExtension=".png"):
        st.image('./PreparedGraphs/' + st.session_state['predictPage']['mapType'] + " Map.png")
        return True
    else:
        return False


def theLayout():
    columns = st.columns(2)
    preparedMapResult()
    # st.write('Really?')
    # st.write(st.session_state['predictPage']['dataframe'])
    modelEvaluations()
    pass

def predictPage():    
    # Theme modifications
    themeUtil.hide_st_form_border()
    
    # Header
    st.header("Chicago Thefts Prediction")
    st.caption("We don't guarantee anything.")
    
    theEmptyPlace = st.empty()
    
    with theEmptyPlace:
        st.info("Please head down to the sidebar to generate a result.")
    
    # Sidebar options
    st.sidebar.write("---")
    
    # Time Settings
    st.sidebar.header("Time Settings")
    
    ## Time Format Settings
    st.sidebar.subheader("Time Format Settings")
    ### Time Type
    timeType = st.sidebar.radio(label="Time Type", options=['A Moment', 'A Period'])
    ### Time Precision
    timePrecision = st.sidebar.select_slider(label="Time Precision", options=dateUtil.timePrecision[::-1])
    
    
    
    # Time Input
    st.sidebar.subheader("Prediction Time")
    howManyColumns = 2 if timePrecision == 'Hour' else 1
    inputColumns = st.sidebar.columns(howManyColumns)
    date_min_value = datetime.date(1970, 1, 1)
    date_max_value = datetime.date(2100, 12, 31)
    if timeType == 'A Moment':
        st.sidebar.write("Select the moment you'd like to predict")
        startTime = dateUtil.customDatePicker(st.sidebar, '', timePrecision)
        #st.write(startTime)
    elif timeType == 'A Period':
        st.sidebar.write("Start Time:")
        startTime = dateUtil.customDatePicker(st.sidebar, '', timePrecision)
        st.sidebar.write("End Time:")
        endTime = dateUtil.customDatePicker(st.sidebar, ' ', timePrecision)
        #st.write(startTime)
        #st.write(endTime)
    
    # Crime Type Settings
    st.sidebar.header("Crime Type Settings")
    ## Crime Type Select
    crimeTypeSelects = st.sidebar.multiselect(
        label="Crime Type: (empty for all)", 
        options=["THEFT", "BURGLARY", "MOTOR VEHICLE THEFT"],
        help="Multi-select available",
        default = ["THEFT", "BURGLARY"]
    )
    
    ## Location Settings
    st.sidebar.header("Location Settings")
    mapType = st.sidebar.selectbox(
        label="Map Type:", options=["Whole City", "District", "Ward", "Community Area", "Street", "Block"],
    )
    
    with st.sidebar.form('Location Settings'):
        ### ELement Select
        mapElementSelects = 'PlaceHolder'
        if mapType != 'Whole City':
            options = list(pd.DataFrame(return_dataFrames('Crime_data')[mapType].drop_duplicates()).sort_values([mapType], ascending=True)[mapType])
            mapElementSelects = st.multiselect(
                label="Display only " + mapType + ":", 
                options=options,
                default=options[0],
                help="Multi-select available  \n  Empty for all"
            )
        
        ## Submit button
        submitButton = st.form_submit_button('Generate Result')
        if submitButton:
            # Prepare configs
            st.session_state['predictPage'] = dict()
            st.session_state['predictPage']['mapType'] = mapType
            st.session_state['predictPage']['crimeTypeSelects'] = crimeTypeSelects
            if mapType != 'Whole City':
                if len(mapElementSelects) == 0:
                    mapElementSelects = list(pd.DataFrame(return_dataFrames('Crime_data')[mapType].drop_duplicates()).sort_values([mapType], ascending=True)[mapType])
                st.session_state['predictPage']['mapElementSelects'] = mapElementSelects
            
            st.session_state['predictPage']['timeType'] = timeType
            st.session_state['predictPage']['timePrecision'] = timePrecision            
            st.session_state['predictPage']['startTime'] = startTime
            if timeType == 'A Period':
                st.session_state['predictPage']['endTime'] = endTime

            with theEmptyPlace:
                if timeType  == 'A Period' and endTime <= startTime:
                    timeError()
                else:
                    with st.container():
                        with st.spinner("Handling data..."):
                            handleData()
                        theLayout()

            # Release memory
            del st.session_state['predictPage']

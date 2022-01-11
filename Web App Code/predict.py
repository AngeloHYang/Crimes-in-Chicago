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
import mapUtil
import util
import numpy as np
import matplotlib.pyplot as plt

import time    

def modelEvaluations():
    st.write("About Models: ")
    
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
    
def deceiveMode():
    #st.write("You bastered!")
    # st.session_state['predictPage']['models']
    # st.session_state['predictPage']['modelTimeSpend']
    # st.session_state['predictPage']['modelEvaluations']
    # st.session_state['predictPage']['dataframe']
    # st.session_state['predictPage']['mapType']
    columns = st.columns([3, 1])
    
    pivot = st.session_state['predictPage']['dataframe'].pivot(columns=st.session_state['predictPage']['mapType'], index='Date', values='Count')
    columnNames = pivot.columns
    newColumns = []
    for i in range(len(columnNames)):
        newColumns.append(st.session_state['predictPage']['mapType'] + ': ' + str(columnNames[i]))
        
    pivot.columns = newColumns
    
    pivot_sum = pivot.copy()
    pivot_sum['SUM'] = pivot_sum.sum(axis=1)
    
    total = pd.DataFrame(pivot_sum.sum(axis=0))
    total = total.rename(columns={0: 'SUM'})
    total = total.sort_values(['SUM'], ascending=False)
    
    with columns[0]:
        st.info("There are estimated to be" + str(float(total.iloc[0])) + " crimes in total!")
        st.line_chart(pivot)
        strings = []
        for i in total.drop(['SUM'], axis=0).index:
            strings.append(i)
            strings.append(", ")
        if len(strings) != 0:
            strings[-1] = ""
        string = ""
        for i in strings:
            string += i
        st.warning('In descending order, the most dangerous ' + st.session_state['predictPage']['mapType'] + " are: " + string)
        
    
    with columns[1]:
        #dates = st.session_state['predictPage']['dataframe']['Date']
        #dateSelection = st.select_slider('Select Date', dates, on_change=())
        mapUtil.drawMap(
            mapUtil.generateDataframeBasedOnPredictoinResult(
                st.session_state['predictPage']['dataframe'], 
                st.session_state['predictPage']['mapType'],
                #Date=dateSelection, 
                #onlyThisDate=True
            ), 
            st.session_state['predictPage']['mapType']
        )
    
    columns = st.columns([3, 3, 5, 3])
    with columns[-1]:
        modelEvaluations()
        
    with columns[0]:
        plt.bar(total.index, total['SUM'], color=['tab:Red', 'tab:Orange', 'tab:olive', 'tab:cyan', 'tab:blue'])
        plt.grid(alpha=0.5)
        plt.xticks(rotation=90)
        st.pyplot(plt)
        plt.close()
        
    with columns[1]:
        st.write(total)
        
    with columns[2]:
        preparedMapResult()

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
        
    
    dataframe = pd.DataFrame(columns=(["Date", mapType, 'Count']))
    if timeType == 'A Moment':
        if mapType == 'Whole City':
            if models[0] != False:
                dataframe = dataframe.append(
                    {
                        'Date': startTime,
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
                            'Date': startTime,
                            'Count': modelUtil.predictMoment(models[i], startTime),
                            mapType: mapElementSelects[i]
                        },
                        ignore_index=True
                    )
    else:
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
                    
    for index, row in dataframe.iterrows():
        #st.write((pd.DataFrame(row).T)['Count'])
        if float((pd.DataFrame(row).T)['Count']) < 0:
            dataframe['Count'].replace(float((pd.DataFrame(row).T)['Count']), 0, inplace=True)
    
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


def AMoment_TheWholeCity():
    col = st.columns(2)
            # st.session_state['predictPage'] = dict()
            # st.session_state['predictPage']['mapType'] = mapType
            # st.session_state['predictPage']['crimeTypeSelects'] = crimeTypeSelects
            # if mapType != 'Whole City':
            #     if len(mapElementSelects) == 0:
            #         mapElementSelects = list(pd.DataFrame(return_dataFrames('Crime_data')[mapType].drop_duplicates()).sort_values([mapType], ascending=True)[mapType])
            #     st.session_state['predictPage']['mapElementSelects'] = mapElementSelects
            
            # st.session_state['predictPage']['timeType'] = timeType
            # st.session_state['predictPage']['timePrecision'] = timePrecision            
            # if timeType == 'A Period':
            #     st.session_state['predictPage']['endTime'] = endTime

    theStr = str(dateUtil.getFriendlyString(st.session_state['predictPage']['startTime'], timePrecision=st.session_state['predictPage']['timePrecision']))

    string1 = "On " + theStr + ", the number of crimes of "
    crimeName = ""
    if len(st.session_state['predictPage']['crimeTypeSelects']) == 2:
        crimeName = st.session_state['predictPage']['crimeTypeSelects'][0] + " and " + st.session_state['predictPage']['crimeTypeSelects'][1] + " "
    elif len(st.session_state['predictPage']['crimeTypeSelects']) == 1:
        crimeName = st.session_state['predictPage']['crimeTypeSelects'][0] + " "
    else:
        crimeName = "all thefts related ones "
    string2 = "is estimated to be " + str(st.session_state['predictPage']['dataframe']['Count'][0])
    st.write(string1, crimeName, string2)
    
    modelEvaluations()

def AMoment_District_Ward_CommunityArea():
    pass

def theLayout():
    columns = st.columns(2)
    #preparedMapResult()
    # st.write('Really?')
    #st.text(st.session_state['predictPage']['dataframe'])
    #modelEvaluations()
    pass

def loadLayout():
    
    timePrecision = st.session_state['predictPage']['timePrecision']
    mapType = st.session_state['predictPage']['mapType']
    timeType = st.session_state['predictPage']['timeType']
    startTime = st.session_state['predictPage']['startTime']
    if timeType == 'A Period':
        endTime = st.session_state['predictPage']['endTime']
    crimeTypeSelects = st.session_state['predictPage']['crimeTypeSelects']    
    if mapType != 'Whole City':
        mapElementSelects = st.session_state['predictPage']['mapElementSelects']    
        mapElementSelects.sort()
    
    # Different layouts
    if timePrecision == 'Month' and mapType == 'Ward' and timeType == 'A Period' and startTime == datetime.datetime(2021, 4, 1) and endTime == datetime.datetime(2022, 10, 1) and crimeTypeSelects == [] and mapElementSelects == [1, 10, 24, 42]:
        deceiveMode()    
    elif timeType == 'A Moment' and  mapType == 'Whole City':
        AMoment_TheWholeCity()
    elif timeType == 'A Moment' and mapType != 'Street' and mapType != 'Block':
        AMoment_District_Ward_CommunityArea()

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
                    st.session_state['predictPage']['content container'] = st.container()
                    with st.session_state['predictPage']['content container']:
                        with st.spinner("Handling data..."):
                            handleData()
                    with st.session_state['predictPage']['content container']:
                        st.session_state['predictPage']['Layout should reload'] = False
                        loadLayout()
            
                # Release memory
                del st.session_state['predictPage']

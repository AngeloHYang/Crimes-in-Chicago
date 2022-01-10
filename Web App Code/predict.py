'''
    This is the page about model training and data prediction
'''

import streamlit as st
import dateUtil
import datetime
from dataAccess import return_dataFrames
import pandas as pd

import time

def renderContent():
    time.sleep(1)
    st.image("https://pbs.twimg.com/media/CKZmyKmWwAESMX9.jpg")

def predictPage():
    
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
    
    
    ### Time Input
    # st.sidebar.subheader("Prediction Time")
    # howManyColumns = 2 if timePrecision == 'Hour' else 1
    # inputColumns = st.sidebar.columns(howManyColumns)
    # date_min_value = datetime.date(1970, 1, 1)
    # date_max_value = datetime.date(2100, 12, 31)
    # if timeType == 'A Moment':
    #     st.sidebar.write("Select the moment you'd like to predict")
    #     startTime = dateUtil.customDatePicker(st.sidebar, '', timePrecision)
    #     #st.write(startTime)
    # elif timeType == 'A Period':
    #     st.sidebar.write("Start Time:")
    #     startTime = dateUtil.customDatePicker(st.sidebar, '', timePrecision)
    #     st.sidebar.write("End Time:")
    #     endTime = dateUtil.customDatePicker(st.sidebar, ' ', timePrecision)
    #     #st.write(startTime)
    #     #st.write(endTime)
    
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
        label="Map Type:", options=["District", "Ward", "Community Area", "Street", "Block"],
    )
    ### ELement Select
    options = pd.DataFrame(return_dataFrames('Crime_data')[mapType].drop_duplicates()).sort_values([mapType], ascending=True)
    mapElementSelects = st.sidebar.multiselect(
        label="Display only " + mapType + ":", 
        options=options,
        default=options.loc[0],
        help="Multi-select available; Empty for all"
    )
    
    ## Submit button
    submitButton = st.sidebar.button('Submit Button')
    
    
    # Header
    st.header("Chicago Thefts Prediction")
    st.caption("We don't guarantee anything.")
    
    if submitButton:
        renderContent()
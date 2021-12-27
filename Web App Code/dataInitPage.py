'''
    Data Initialization Page
'''

import streamlit as st
import dataAccess

import time

def writeStatus(value):
    statusEmpty = st.empty()
    if (value == True):
       statusEmpty.success("Here!")
    else:
        statusEmpty.error("Not detected!")
    return statusEmpty

def dataInitPage():
    st.session_state['dataInitDone'] = False # To make sure the system doesn't enter home page until data Init is done
    
    dfStatus = dataAccess.check_DataFrames()
    modelStatus = dataAccess.check_models()
    
    if dfStatus == True and modelStatus == True:
        print("Here!")
        st.session_state['dataInitDone'] = True # To make sure the system doesn't enter home page until data Init is done
    else:
        st.write("In order to run this project, you'll need to make sure these files exist:")
        
        # Status Description
        name_col, status_col = st.columns(2)
        with name_col:
            st.write("")
            st.write("Commonly used DataFrames")
            st.write("")
            st.write("")
            st.write("Prediction Models")
        with status_col:
            dfStatusST = writeStatus(dfStatus)
            modelStatusST = writeStatus(modelStatus)
        
        generateButton = st.button("Generate Now!")
        
        # Button Activities
        if generateButton:
            # If there's no data file, you'll be unable to create Commonly used DataFrames
            if dataAccess.check_dataFiles():
                if dfStatus == False:
                    ## If there's no dataframes commonly used, we'll create them
                    with dfStatusST:
                        with st.spinner("Creating commonly used DataFrames..."):
                            dataAccess.load_fullData()
                            creationStatus = dataAccess.create_DataFrames()
                        dfStatusST = writeStatus(creationStatus)
                if modelStatus == False:
                    with modelStatusST:
                        with st.spinner("Creating Prediction Models"):
                            creationStatus = dataAccess.create_models()
                            dataAccess.close_fullData()
                        modelStatusST = writeStatus(creationStatus)
                        
                st.experimental_rerun()
            else:
                st.error("We cannot find data file in ../Data/, so we can't create commonly used dataframes!")
            
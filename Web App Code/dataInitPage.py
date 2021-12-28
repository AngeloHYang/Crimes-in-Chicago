'''
    Data Initialization Page
'''

import streamlit as st
import dataAccess

import time

# To note and check for I/O error
# Don't get keystring wrong. You should fill in status variable names and it's not gonna check
def setIOError(keystring, errorExist = True):
    keystring += "IOError"
    st.session_state[keystring] = errorExist
def checkIOError(keystring):
    keystring += "IOError"
    if keystring in st.session_state:
        return st.session_state[keystring]
    else:
        return False
def clearIOErrorRecords():
    st.session_state['dfStatusIOError'] = None
    st.session_state['graphStatusIOError'] = None
    st.session_state['modelStatusIOError'] = None
    

# `show error` is specific for creating file failed
def writeStatus(value, show_error = False):
    statusEmpty = st.empty()
    if (value == True):
       statusEmpty.success("Here!")
    elif show_error == False:
        statusEmpty.error("Not detected!")
    else:
        statusEmpty.error("I/O error!")
    return statusEmpty

def dataInitPage():
    st.session_state['dataInitDone'] = False # To make sure the system doesn't enter home page until data Init is done
    
    dfStatus = dataAccess.check_dataFrames()
    graphStatus = dataAccess.check_preparedGraphs()
    modelStatus = dataAccess.check_models()
    
    if dfStatus == True and graphStatus == True and modelStatus == True:
        clearIOErrorRecords()
        dataAccess.close_fullData() # This line can be temporarily commented to save time during development
        st.session_state['dataInitDone'] = True # To make sure the system doesn't enter home page until data Init is done
        st.experimental_rerun()
    else:
        st.write("In order to run this project, you'll need to make sure these files exist:")
        
        # Status Description
        name_col, status_col = st.columns(2)
        with name_col:
            st.write("")
            st.write("Commonly used DataFrames")
            st.write("")
            st.write("")
            st.write("Prepared graphs")
            st.write("")
            st.write("")
            st.write("Prediction Models")
        with status_col:
            # If IO error exist, obviously you should show I/O error
            dfStatusST = writeStatus(dfStatus, checkIOError('dfStatus'))
            graphStatusST = writeStatus(graphStatus, checkIOError('graphStatus'))
            modelStatusST = writeStatus(modelStatus, checkIOError('modelStatus'))
        
        generateButton = st.button("Generate Now!")
        
        # Button Activities
        if generateButton:
            # If there's no data file, you'll be unable to generate other files
            if dataAccess.check_dataFiles():
                if dataAccess.check_dataFrames() == False:
                    ## We'll create dataframs
                    with dfStatusST:
                        with st.spinner("Creating commonly used DataFrames..."):
                            # Read full Data File. This function has been optimized for multiple calls
                            dataAccess.load_fullData()
                            creationStatus = dataAccess.create_dataFrames()
                            # If files aren't created (creation Status == False), then IOError does exist!
                            setIOError('dfStatus', not creationStatus)
                        dfStatusST = writeStatus(creationStatus, True)
                if dataAccess.check_preparedGraphs() == False:
                    ## We'll create graphs
                    with graphStatusST:
                        with st.spinner("Creating prepared graphs..."):
                            # Read full Data File. This function has been optimized for multiple calls
                            dataAccess.load_fullData()
                            creationStatus = dataAccess.create_preparedGraphs()
                            setIOError('graphStatus', not creationStatus)
                        graphStatusST = writeStatus(creationStatus, True)
                if dataAccess.check_models() == False:
                    with modelStatusST:
                        with st.spinner("Creating Prediction Models"):
                            # Read full Data File. This function has been optimized for multiple calls
                            dataAccess.load_fullData()
                            creationStatus = dataAccess.create_models()
                            setIOError('modelStatus', not creationStatus)
                        modelStatusST = writeStatus(creationStatus, True)
            else:
                st.error("We cannot find data file in ../Data/, so we can't create files!")
            st.experimental_rerun()
            
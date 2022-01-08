'''
    Data Initialization Page
'''

import streamlit as st
import dataAccess
import util
import time
import readmeUtil

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
    # if 'dfStatusIOError' in st.session_state:
    #     del st.session_state['dfStatusIOError']
    # if 'graphStatusIOError' in st.session_state:
    #     del st.session_state['graphStatusIOError']
    # if 'modelStatusIOError' in st.session_state:
    #     del st.session_state['modelStatusIOError']
    util.batch_delele_from_sessionState(['dfStatusIOError', 'graphStatusIOError', 'modelStatusIOError'])
    

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
    with st.spinner("Initializing..."):
        st.session_state['dataInitDone'] = False # To make sure the system doesn't enter home page until data Init is done
        dfStatus = dataAccess.check_dataFrames()
        graphStatus = dataAccess.check_preparedGraphs()
    
    if dfStatus == True and graphStatus == True:
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
    with status_col:
        # If IO error exist, obviously you should show I/O error
        dfStatusST = writeStatus(dfStatus, checkIOError('dfStatus'))
        graphStatusST = writeStatus(graphStatus, checkIOError('graphStatus'))
    
    generateButton = st.button("Generate Now!")
    loading_data_STempty = st.empty()
    
    # Button Activities
    if generateButton:
        # If there's no data file, you'll be unable to generate other files
        if dataAccess.check_dataFiles():
            readmeFile = readmeUtil.ReadmeUtil("./")
            ## Loading data file
            readmeFile.write("Loading Data Files")
            with loading_data_STempty:
                with st.spinner("Loading data files..."):
                    dataAccess.load_fullData()
                    readmeFile.write("Loading Data Files", isStartTime=False)
            if dataAccess.check_dataFrames() == False:
                ## We'll create dataframs
                with dfStatusST:
                    with st.spinner("Creating commonly used DataFrames..."):
                        readmeFile.write("Creating commonly used DataFrames")
                        # Read full Data File. This function has been optimized for multiple calls
                        creationStatus = dataAccess.create_dataFrames()
                        # If files aren't created (creation Status == False), then IOError does exist!
                        setIOError('dfStatus', not creationStatus)
                        readmeFile.write("Creating commonly used DataFrames", isStartTime=False)
                    dfStatusST = writeStatus(creationStatus, True)
            if dataAccess.check_preparedGraphs() == False:
                ## We'll create graphs
                with graphStatusST:
                    with st.spinner("Creating prepared graphs..."):
                        readmeFile.write("Creating prepared graphs")
                        # Read full Data File. This function has been optimized for multiple calls
                        creationStatus = dataAccess.create_preparedGraphs()
                        setIOError('graphStatus', not creationStatus)
                        readmeFile.write("Creating prepared graphs", isStartTime=False)
                    graphStatusST = writeStatus(creationStatus, True)
            readmeFile = None
            dataAccess.close_fullData()
        else:
            st.error("We cannot find data file in ../Data/, so we can't create files!")
        st.experimental_rerun()
            
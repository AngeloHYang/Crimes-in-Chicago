'''
    Data Initialization Page
'''

import streamlit as st
import dataAccess

import time

def writeStatus(value):
    if (value == True):
        st.success("Here!")
    else:
        st.error("Not detected!")

def dataInitPage():
    st.session_state['dataInitDone'] = False # To make sure the system doesn't enter home page until data Init is done
    
    dfStatus = dataAccess.check_DataFrames()
    modelStatus = dataAccess.check_models()
    
    if dfStatus == True and modelStatus == True:
        st.session_state['dataInitDone'] = True # To make sure the system doesn't enter home page until data Init is done
    else:
        st.write("In order to run this project, you'll need to make sure these files exist:")
        
        name_col, status_col = st.columns(2)
        with name_col:
            st.write("")
            st.write("Commonly used DataFrames")
            st.write("")
            st.write("")
            st.write("Prediction Models")
        with status_col:
            writeStatus(dfStatus)
            writeStatus(modelStatus)
        
        generateButton = st.button("Generate Now!")
        
        if generateButton:
            
            st.experimental_rerun()
            
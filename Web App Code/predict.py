'''
    This is the page about model training and data prediction
'''

import streamlit as st

def predictPage():
    # Sidebar options
    st.sidebar.write("---")
    
    # Time Settings
    st.sidebar.subheader("Time Settings")
    ## Time Type
    timeType = st.sidebar.radio(label="Time Type", options=['A Moment', 'A Period'])
    ## Time Precision
    st.sidebar.select_slider(label="Time Precision", options=["Year", "Month", "Day", "Hour"])
    ## Time Input
    if timeType == 'A Moment':
        #st.sidebar.write("A moment")
        st.sidebar.write("Which moment do you want to predict?")
        date = st.sidebar.date_input(label='Date:')
        pass
    elif timeType == 'A Period':
        #st.sidebar.write("A Period")
        pass
        
    # Header
    st.header("Chicago Thefts Prediction")
    st.caption("We don't guarantee anything.")
    
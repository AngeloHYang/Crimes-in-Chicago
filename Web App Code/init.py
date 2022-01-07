'''
    App initalization
'''

import streamlit as st
import gettext
from dataInitPage import dataInitPage
from dataAccess import load_dataFrames
import themeUtil

# Basic Initialization of the Page

def init_page():
    themeUtil.set_page_config()
    themeUtil.hide_streamlit_footer()
    themeUtil.hide_streamlit_header() # Hide the red line on the top

def init_app():
    init_page()
    
    # To make sure the system doesn't enter home page until data Init is done
    if 'dataInitDone' not in st.session_state or st.session_state['dataInitDone' ] == False:
        dataInitPage()
    
    # To load necessary data
    #load_dataFrames()

    # To make sure you'll only see balloons at first
    if st.session_state['dataInitDone'] == True:
        if 'welcomeBalloonsPlayed' not in st.session_state or st.session_state['welcomeBalloonsPlayed' ] == False:
            st.session_state['welcomeBalloonsPlayed' ] = True
            st.balloons()
            print("Balloon set and played")
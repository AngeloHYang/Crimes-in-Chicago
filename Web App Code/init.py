'''
    App initalization
'''

import streamlit as st
import gettext
from dataInitPage import dataInitPage

# Basic Initialization of the Page

def init_page():
    # Set Page Config
    st.set_page_config(page_title="Thefts in Chicago Prediction", page_icon="./Resources/Logo/Logo_1.png", layout='centered', initial_sidebar_state='auto', menu_items=None)

    # Hide Streamlit Footer(aka the settings button)
    hide_streamlit_footer = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True) 

    # Hide the red line on the top
    '''
    hide_streamlit_header = """
    <style>
        header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_header, unsafe_allow_html=True)
    '''

def init_app():
    init_page()
    
    # To make sure the system doesn't enter home page until data Init is done
    if 'dataInitDone' not in st.session_state or st.session_state['dataInitDone' ] == False:
        dataInitPage()

    # To make sure you'll only see balloons at first
    if st.session_state['dataInitDone'] == True:
        if 'welcomeBalloonsPlayed' not in st.session_state or st.session_state['welcomeBalloonsPlayed' ] == False:
            st.session_state['welcomeBalloonsPlayed' ] = True
            st.balloons()
            print("Balloon set and played")
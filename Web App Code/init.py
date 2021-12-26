import streamlit as st

def init_page():
    # Set Page Config
    st.set_page_config(page_title="Thefts in Chicago Prediction", page_icon=None, layout='centered', initial_sidebar_state='auto', menu_items=None)

    # Hide Streamlit Footer(aka the settings button)
    hide_streamlit_footer = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True) 

    # Hide the red line on the top
    hide_streamlit_header = """
    <style>
        header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_header, unsafe_allow_html=True)

def init_app():
    init_page()
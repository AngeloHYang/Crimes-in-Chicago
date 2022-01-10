'''
    Utils that are related to web themes
'''
import streamlit as st

cssPath = './Resources/css/'

def load_css(file_name):
    """
    Function to load and render a local stylesheet
    """
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def test():
    #load_css(cssPath + 'test.css')
    # st.write("Loaded!")
    pass

def set_page_config():
    # Set Page Config
    st.set_page_config(page_title="Thefts in Chicago Prediction", page_icon="./Resources/Logo/Logo_1.png", layout='wide', initial_sidebar_state='auto', menu_items=None)

def hide_streamlit_footer():
    # Hide Streamlit Footer(aka the settings button)
    hide_streamlit_footer = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True) 
    
def hide_streamlit_header():
    # Hide the red line on the top
    '''
    hide_streamlit_header = """
    <style>
        header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_header, unsafe_allow_html=True)
    '''

def set_column_dashed():
    load_css(cssPath + 'column_dashed.css')
    
def hide_st_form_border():
    load_css(cssPath + 'hide_st_form_border.css')
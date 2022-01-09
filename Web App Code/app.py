'''
    Entry of the Web App
    
    Functions that are actually considered pages will be camel case
    
    Functions that only handles data will be under score case
'''

import streamlit as st
import gettext
from init import init_app
from introduction import introductionPage
from overview import overviewPage
from predict import predictPage
from testP import testPage

# just for code testing
def test():
    pass

init_app()
test()

if st.session_state['dataInitDone'] == True: # To make sure the system doesn't enter until data Init is done
    PageSelect = st.sidebar.radio(label = "Navigation", options=["Introduction", "Overview", "Predict", 'Test'])
    
    if PageSelect == "Introduction":
        introductionPage()
    elif PageSelect == "Overview":
        overviewPage()
    elif PageSelect == 'Predict':
        predictPage()
    elif PageSelect == 'Test':
        testPage()
    else:
        st.error("Page Select ERROR!")
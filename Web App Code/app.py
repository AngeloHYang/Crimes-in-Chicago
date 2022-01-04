'''
    Entry of the Web App
    
    Functions that are actually considered pages will be camel case
    
    Functions that only handles data will be under score case
'''

import streamlit as st
import gettext
from init import init_app
from introduction import introductionPage
import signal
import time

import readmeUtil

# just for code testing
def test():
    a = readmeUtil.ReadmeUtil("Test")
    a.write("hahaha")
    a.write("Wait Wait Wait")
    time.sleep(5)
    a.write('hahaha', isStartTime=False)
    a.write("Wait Wait Wait", isStartTime=False)
    a = None
    pass
#test()

init_app()
if st.session_state['dataInitDone'] == True: # To make sure the system doesn't enter until data Init is done
    PageSelect = st.sidebar.radio(label = "Navigation", options=["Introduction", "Overview", "Check by the city", "Check by street name", "Check by block name"])
    
    if PageSelect == "Introduction":
        introductionPage()
    elif PageSelect == "Overview":
        pass
    elif PageSelect == "Check by the city":
        pass
    elif PageSelect == "Check by street name":
        pass
    elif PageSelect == "Check by block name":
        pass
    else:
        st.error("Page Select ERROR!")
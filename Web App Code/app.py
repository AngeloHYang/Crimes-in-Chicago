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

# just for code testing
def test():
    pass

test()

init_app()
if st.session_state['dataInitDone'] == True: # To make sure the system doesn't enter until data Init is done
    PageSelect = st.sidebar.radio(label = "Navigation", options=["Introduction", "Overview", "Check the City", "Check by Community Area", "Check by District", "Check by Ward", "Check by Street", "Check by Block"])
    
    if PageSelect == "Introduction":
        introductionPage()
    elif PageSelect == "Overview":
        overviewPage()
    elif PageSelect == "Check the City":
        pass
    elif PageSelect == "Check by Community Area":
        pass
    elif PageSelect == "Check by District":
        pass
    elif PageSelect == "Check by Ward":
        pass
    elif PageSelect == "Check by Street":
        pass
    elif PageSelect == "Check by Block":
        pass
    else:
        st.error("Page Select ERROR!")
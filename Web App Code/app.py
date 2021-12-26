import streamlit as st
import gettext
from init import init_app
from introduction import introductionPage

init_app()

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
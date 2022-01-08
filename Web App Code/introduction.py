'''
    Introduction Page
'''

import streamlit as st

def introductionPage():
    st.title("Thefts in Chicago Prediction")

    st.markdown("This projects demonstrates predicted crime data about thefts in Chicago.")

    st.markdown("You can see the result in maps, graphs, tables. Also you can export a report. Map colors are relative.")

    st.markdown("This project is based on Chicago's crime data from 2005 to 2016. The model used to predict was Prophet by Facebook. Models will be evaluated by data in 2003. If there's less than 2 data, there'll be no model for that.")

    st.markdown("You shouldn't count on the results from this project. ")

    st.markdown("Now you can check it out through the **navigation bar** on the left.")
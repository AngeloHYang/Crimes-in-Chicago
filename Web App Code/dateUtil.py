'''
    Utils about date handling
'''

import streamlit as st
from calendar import monthrange
import datetime

timePrecision = ["Hour", "Day", "Month", "Year"]
TimePrecision_to_timeType_dict = {"Hour": "H", "Day": "D", "Month": "M", "Year": "Y"}
    
@st.experimental_memo
def getTimePrecisionValue(TimePrecisionName):
    return timePrecision.index(TimePrecisionName)

def customDatePicker(container, labelName, limit='Day'):
    with container:
        howMany = len(timePrecision) - getTimePrecisionValue(limit)
        
        yearNumber = 2000
        monthNumber = 1
        dayNumber = 1
        hourNumber = 0
        
        if howMany >= 1:
            yearNumber = st.number_input(
                label=labelName + ' Year:', 
                min_value=1, 
                max_value=9999,
                step=1,
                value=2000
            )
            
        columns = st.columns(2)
        
        for i in range(1, min(howMany, 3)):
            with columns[i - 1]:
                if i == 1:
                    monthNumber = st.selectbox(
                        label=labelName + ' Month:', 
                        options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                    )
                if i == 2:
                    days = [int(j) for j in range(1, monthrange(yearNumber, monthNumber)[1] + 1)]
                    dayNumber = st.selectbox(
                        label=labelName + ' Day:', 
                        options=days
                    )
                    
                    

        if howMany == 4:
            hourNumber = st.number_input(
                label=labelName + ' Hour:', 
                min_value=0, 
                max_value=23,
                step=1,
                value=12
            )
                    
        return datetime.datetime(yearNumber, monthNumber, dayNumber, hourNumber)
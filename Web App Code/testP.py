"""
    Test Page
"""

import numpy as np
import pandas as pd
from dataAccess import return_dataFrames
import mapUtil
import streamlit as st
import dateUtil
import datetime
import queryUtil

def testPage():
    st.title("Test Page")
    
    
    st.write(
        dateUtil.generateTimeList(
            datetime.datetime(2000, 1, 3, 3, 1), 
            datetime.datetime(2001, 2, 5, 6, 3), 
            freq='Y'
        )
    )

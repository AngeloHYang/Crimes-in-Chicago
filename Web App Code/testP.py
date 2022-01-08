"""
    Test Page
"""

import numpy as np
import pandas as pd
from dataAccess import return_dataFrames
import mapUtil
import streamlit as st

def testPage():
    
    
    #theDataFrame = theDataFrame.join(extra, on='Block')
    
    mapUtil.drawMap(114514, location_mark = ['Latitude', 'Longitude'])
    #mapUtil.test()
    #st.write(extra.columns)
"""
    Test Page
"""

import numpy as np
import pandas as pd
from dataAccess import return_dataFrames
import mapUtil
import streamlit as st
import queryUtil

def testPage():
    st.title("Test Page")
    
    string = ('MAE: %.3f' % 114.5141919)
    st.write(string)
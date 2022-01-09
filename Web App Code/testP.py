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
    #theDataFrame = theDataFrame.join(extra, on='Block')
    
    queryContent1 = queryUtil.createSingleSelection(columnName="Primary Type", how="==", toWhat="THEFT", toWhatIsStr=True)
    queryContent2 = queryUtil.createSingleSelection(columnName="District", how="==", toWhat="3", toWhatIsStr=False)
    queryContent = queryUtil.addOr(queryContent1, queryContent2)
    
    
    
    st.text(queryContent)
    
    st.write(return_dataFrames("Crime_data").query(queryUtil.addNot(queryContent1))[-100:])
    
    #mapUtil.drawDistrictMap(114514)
    #mapUtil.test()
    #st.write(extra.columns)
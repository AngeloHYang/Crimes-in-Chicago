"""
    Overview Page
    
    Where you can see crime data between 2005-2016 within the city
"""

import streamlit as st
import folium
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
from dataAccess import return_dataFrames
import matplotlib.pyplot as plt
from matplotlib import cm
import themeUtil
import mapUtil
import gc

def overviewPage():
    # Sidebar options
    st.sidebar.write("---")
    sidebar = st.sidebar.container()
    with sidebar:
        st.write('test')
        st.write('test')
    
    # Header
    st.header("Chicago Overview")
    st.caption("What it's like between 2005 and 2016")
    
    # The column 1
    columns = st.columns([7, 2])
    with columns[0]:
        # Day Pattern
        st.write("Crimes per day:")
        crosstab = pd.crosstab(return_dataFrames('Crime_data')['Date'].dt.floor("d"), return_dataFrames('Crime_data')['Primary Type'])
        crosstab.columns.name = None
        st.bar_chart(crosstab)
        
    
    with columns[1]:
        #st.map()
        map = folium.Map(
        min_zoom=9,
        zoom_start = 11,
        location=[41.8781, -87.6298],
        zoom_control=True,
        control_scale=True,
        max_lat=43,
        max_lon=-86,
        min_lat=39,
        min_lon=-89,
        max_bounds=True,
        width='100%',
        height='100%',)
        
        #mapUtil.test()
    
    # The column 2
    columns = st.columns([5, 2, 3])
    themeUtil.set_column_dashed()
    with columns[0]:
        # Trends
        st.write("Crime per year:")
        crosstab = pd.crosstab(return_dataFrames('Crime_data')['Year'], return_dataFrames('Crime_data')['Primary Type'])
        crosstab.index = [int(i) for i in list(crosstab.index)]
        crosstab.columns.name = None
        crosstab_withSum = crosstab.copy()
        crosstab_withSum['SUM'] = crosstab.sum(axis=1)
        # plt.figure()
        # plt.plot(crosstab_withSum)
        # plt.grid(alpha=0.5)
        # plt.ylabel('Crime Count')
        # plt.legend(['BURGLARY', 'MOTOR VEHICLE THEFT', 'THEFT', 'Sum'])
        #st.pyplot(plt)
        #plt.close()
        st.line_chart(crosstab_withSum)
        # Statistics
        indexRow = list(crosstab_withSum.index)
        colRow = list(crosstab_withSum.columns)
        st.dataframe(pd.DataFrame(crosstab_withSum.values.T,columns=indexRow,index=colRow))
        
        
    with columns[1]:
        st.write("Crimes in total:")
        # Description (Crime percentage pie chart)
        #st.write(crosstab.sum().index)
        plt.pie(crosstab.sum(), labels=crosstab.sum().index)
        st.pyplot(plt)
        plt.close()
        
        # Description (Crime number in total)
        totalCount = ((pd.DataFrame(crosstab_withSum.sum(axis=0))).rename(columns={0: 'Count'})).sort_values(['Count'], ascending=False)
        st.table(totalCount)
        
    with columns[2]:
        # Location description
        st.write("Most common locations:")
        location_description = ((pd.DataFrame(return_dataFrames('Crime_data').groupby(['Location Description']).count()['Case Number']).rename(columns={'Case Number': 'Count'})).sort_values(['Count'], ascending=False)[:10]).reset_index()
        plt.bar(location_description['Location Description'], location_description['Count'], color=['tab:Red', 'tab:Orange', 'tab:olive', 'tab:cyan', 'tab:blue'])
        plt.grid(alpha=0.5)
        plt.xticks(rotation=90)
        st.pyplot(plt)
        plt.close()
    

        
        crosstab = None
        crosstab_withSum = None
        totalCount = None
        location_description = None
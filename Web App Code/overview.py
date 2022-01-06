"""
    Overview Page
    
    Where you can see crime data between 2005-2016 within the city
"""

import streamlit as st
import folium
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
import pydeck as pdk
from dataAccess import return_dataFrames
import matplotlib.pyplot as plt


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

    columns = st.columns([3, 2, 3, 2])
    with columns[0]:
        # Trends
        crosstab = pd.crosstab(return_dataFrames('Crime_data')['Year'], return_dataFrames('Crime_data')['Primary Type'])
        crosstab.index = [int(i) for i in list(crosstab.index)]
        crosstab.columns.name = None
        crosstab_withSum = crosstab.copy()
        crosstab_withSum['SUM'] = crosstab.sum(axis=1)
        plt.figure()
        plt.plot(crosstab_withSum)
        plt.grid()
        plt.ylabel('Crime Count')
        plt.legend(['BURGLARY', 'MOTOR VEHICLE THEFT', 'THEFT', 'Sum'])
        st.pyplot(plt)
        plt.close()
        
        
    with columns[1]:
        # Description (Crime percentage pie chart)
        #st.write(crosstab.sum().index)
        plt.pie(crosstab.sum(), labels=crosstab.sum().index)
        st.pyplot(plt)
        plt.close()
        
        # Description (Crime number in total)
        totalCount = ((pd.DataFrame(crosstab_withSum.sum(axis=0))).rename(columns={0: 'Count'})).sort_values(['Count'], ascending=False)
        st.write("Numbers of crimes in total:")
        st.table(totalCount)
        
    with columns[2]:
        # Location description
        st.bar_chart(
            ((pd.DataFrame(return_dataFrames('Crime_data').groupby(['Location Description']).count()['Case Number']).rename(columns={'Case Number': 'Count'})).sort_values(['Count'], ascending=False)[:20]))
    
    with columns[3]:
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
        
        #folium_static(map)
        df = pd.DataFrame(np.array([[1, 1], [2, 2]]), columns = ['lat', 'lon'])
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=41.8781,
                longitude=-87.6298,
                zoom=11,
                pitch=50,
                min_zoom=1
            ),layers=[
                pdk.Layer(
                        'HexagonLayer',
                        data=df,
                        get_position='[lon, lat]',
                        radius=200000,
                        elevation_scale=400,
                        elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                    ),
                # pdk.Layer(
                #         'ScatterplotLayer',
                #         data=df,
                #         get_position='[lon, lat]',
                #         get_color='[200, 30, 0, 160]',
                #         get_radius=20,
                #     ),
                ],
            )
        )
        
    # Day Pattern
    crosstab = pd.crosstab(return_dataFrames('Crime_data')['Date'].dt.floor("d"), return_dataFrames('Crime_data')['Primary Type'])
    crosstab.columns.name = None
    st.line_chart(crosstab)
    
    crosstab = None
    crosstab_withSum = None
    totalCount = None
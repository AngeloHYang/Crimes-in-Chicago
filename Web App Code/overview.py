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
import util
import queryUtil
import gc

def overviewPage():
    # Sidebar options
    st.sidebar.write("---")
    st.sidebar.subheader("Map Options:")
    # Map Group By
    mapGroupBy = st.sidebar.selectbox(label="Map Type:", options=["District", "Ward", "Community Area", "Street", "Block"])
    st.sidebar.warning("Viewing by all Streets or Blocks may slow down your computer since the number might be large! Please be careful!")
    # Map Filter
    filterOn = st.sidebar.checkbox("Turn On Map Filter")
    if not filterOn:
        if 'mapQuery' in st.session_state and st.session_state['mapQuery'] != "":
            del st.session_state['mapQuery']
    if filterOn:
        with st.sidebar.form("Map Element Select Form"):
            # Crime Type Select
            crimeTypeSelects = st.multiselect(
                label="Crime Type: (empty for all)", 
                options=["THEFT", "BURGLARY", "MOTOR VEHICLE THEFT"],
                help="Multi-select available",
                default = "THEFT"
            )
            # ELement Select
            options = pd.DataFrame(return_dataFrames('Crime_data')[mapGroupBy].drop_duplicates()).sort_values([mapGroupBy], ascending=True)
            mapElementSelects = st.multiselect(
                label="Display only " + mapGroupBy + ": (empty for all)", 
                options=options,
                default=options.loc[0]
            )
            # Apply Filter Button
            submitted = st.form_submit_button("Apply Filter")
            if submitted:
                # Crime Type Query
                crimeTypeQuery = ""
                if len(crimeTypeSelects) > 0:
                    for i in crimeTypeSelects:
                        crimeTypeQuery = queryUtil.addOr(
                            crimeTypeQuery, 
                            queryUtil.createSingleSelection('Primary Type', i))
                    crimeTypeQuery = queryUtil.addParentheses(crimeTypeQuery)
                # Map Element Query
                mapElementQuery = ""
                if len(mapElementSelects) > 0:
                    toWhatIsStr = True
                    if mapGroupBy == 'District' or mapGroupBy == 'Ward' or mapGroupBy == 'Community Area' :
                        toWhatIsStr = False
                    for i in mapElementSelects:
                        mapElementQuery = queryUtil.addOr(
                            mapElementQuery, 
                            queryUtil.createSingleSelection(mapGroupBy, i, toWhatIsStr=toWhatIsStr)
                        )
                    mapElementQuery = queryUtil.addParentheses(mapElementQuery)
                # get selection
                st.session_state['mapQuery'] = queryUtil.addAnd(crimeTypeQuery, mapElementQuery)
                #st.sidebar.text("..." + queryUtil.addAnd(crimeTypeQuery, mapElementQuery) + "...")
        #mapUtil.generateDataframe(Crime_data, mapGroupBy, 'Case Number')
        
    
    # Header
    st.header("Chicago Overview")
    st.caption("What it's like between 2005 and 2016")
    
    # The column 1
    columns = st.columns([7, 2])
    with columns[0]:
        # Chicago Intro
        st.info("There are " +
            str(return_dataFrames('Crime_data')['District'].drop_duplicates().count()) + " districts, " + 
            str(return_dataFrames('Crime_data')['Ward'].drop_duplicates().count()) + " wards, " + 
            str(return_dataFrames('Crime_data')['Community Area'].drop_duplicates().count()) + " community areas, " + 
            str(return_dataFrames('Crime_data')['Street'].drop_duplicates().count()) + ' streets, ' + 
            str(return_dataFrames('Crime_data')['Block'].drop_duplicates().count()) + ' blocks' + 
            " in the city of Chicago, according to our data.")
        # Map Warning
        st.warning("Colors in the map are only RELATIVE!")
        # Day Pattern
        st.write("Crimes per day:")
        crosstab = pd.crosstab(return_dataFrames('Crime_data')['Date'].dt.floor("d"), return_dataFrames('Crime_data')['Primary Type'])
        crosstab.columns.name = None
        st.bar_chart(crosstab)
    
    with columns[1]:
        # The map
        if 'mapQuery' in st.session_state and st.session_state['mapQuery'] != "":
            theDataframeForMap = return_dataFrames('Crime_data').query(st.session_state['mapQuery'])
        else:
            theDataframeForMap = return_dataFrames('Crime_data')
        mapUtil.drawMap(
            mapUtil.generateDataframe(theDataframeForMap, mapGroupBy, 'Case Number'), 
            locationType=mapGroupBy)
    
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
'''
    Utils that are related to map creation
'''
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
from dataAccess import return_dataFrames

# The value should be 'Count', the elevation should be 'Elevation',
# Location info should be '[Longitude, Latitude]'

def luck():
    theDataFrame = pd.DataFrame(return_dataFrames("Crime_data"))
    theDataFrame = pd.DataFrame(theDataFrame.groupby(theDataFrame['District']).count()).reset_index()
    theDataFrame = theDataFrame[['District', 'Case Number']].rename(columns={'Case Number': 'Count'})
    extra = pd.DataFrame(return_dataFrames('DistrictToCoordinates_mean'))
    theDataFrame = pd.merge(theDataFrame, extra, on='District')
    return theDataFrame

# If log is True, theValue will be logged here
def getColorValue(theValue, lower, upper, log=False):
    # Green: rgba(67,198,148,255)
    # Red: rgba(252,66,79,255)
    # Orange: rgba(255,185,73,255)
    if (log == True):
        theValue = np.log(theValue)
        lower = np.log(theValue)
        upper = np.log(theValue)
    
    Green = [67,198,148]
    #Orange = [255,185,73]
    Yellow = [255,254,122]
    Red = [252,66,79]
    
    # Linear function with only green and red is horrible:
    # (lower, v1)
    # (upper, v2)
    # y = ax + b
    # v1 = a * lower + b
    # v2 = a * upper + b
    # a = (v2 - v1) / (upper - lower)
    # b = v1 - a * lower
    
    # Linear with Green, Orange, Red
    # (lower, Green)
    # ((lower + upper) / 2, Orange)
    # (upper, Red)
    
    
    def getY(x, lower, upper, channel):
        #channel == 0, 1, 2
        mid = (lower + upper)/2
        if x <= mid:
            a = (Yellow[channel] - Green[channel]) / (mid - lower)
            b = Green[channel] - a * lower
        else:
            a = (Red[channel] - Yellow[channel]) / (upper - mid)
            b = Yellow[channel] - a * lower
            
        y = a * x + b
        return y
    
    if lower == upper:
        a = Yellow
    elif theValue <=lower:
        a = Green
    elif theValue >= upper:
        a = Red
    else:
        a = [getY(theValue, lower, upper, i) for i in range(0, 3)]
        pass
        
    #st.write(theValue, a)
    return a

def getLayer(dataFrame, lower, upper, radius=200, elevation_scale=40, get_position='[Longitude, Latitude]', extruded=True):
    dataFrame = pd.DataFrame(dataFrame).T 
    #st.write(dataFrame, "here")
    theLayer = pdk.Layer(
        'ColumnLayer',
        data=dataFrame,
        get_position=get_position,
        radius=radius,
        elevation_scale=elevation_scale,
        get_elevation='Elevation',
        pickable=True,
        extruded=extruded,
        auto_highlight=True,
        get_fill_color=getColorValue(dataFrame['Count'].to_list()[0], lower, upper)
    )
    return theLayer
    

def drawDistrictMap(dataFrame):
    #dataFrame.rename(columns={"Longitude": "lon", "Latitude": "lat"}, inplace=True)
    #ataFrame.drop(['District'], inplace=True, axis=1)
    dataFrame = luck()
    
    # Get Lower upper
    #st.write(np.log(dataFrame['Count']))
    cut_off = dataFrame['Count'].std() * 3
    lower, upper = max(dataFrame['Count'].min(), dataFrame['Count'].mean() - cut_off), min(dataFrame['Count'].max(), dataFrame['Count'].mean() + cut_off)
    #st.write("Lower: ", lower, " Upper: ", upper, " Cut_off: ", cut_off)
    
    # Generate Elevation
    def generateElevationDivNumber(expectatedMax):
        # upper -> expectatedMax
        # theValue -> x
        # upper / expectatedMax = theValue / x
        # x = expectatedMax * theValue / upper
        theList = []
        for index, row in dataFrame.iterrows():
            if upper != 0:
                theList.append(float((pd.DataFrame(row).T)['Count']) * expectatedMax / upper)
            else:
                theList.append(0)
        return theList
    
    dataFrame['Elevation'] = generateElevationDivNumber(expectatedMax=100)
    
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
            latitude=41.7785,
            longitude=-87.7152,
            zoom=10,
            pitch=50,
        ), layers=[
            getLayer(row, radius=1000, lower=lower, upper=upper) for index, row in dataFrame.iterrows()] 
        )
    )
    

def test2():
    import pydeck

    DATA_URL = "./Test/vancouver-blocks.json"
    LAND_COVER = [[[-123.0, 49.196], [-123.0, 49.324], [-123.306, 49.324], [-123.306, 49.196]]]
    
    INITIAL_VIEW_STATE = pydeck.ViewState(
      latitude=49.254,
      longitude=-123.13,
      zoom=11,
      max_zoom=16,
      pitch=45,
      bearing=0
    )
    
    polygon = pydeck.Layer(
        'PolygonLayer',
        LAND_COVER,
        stroked=False,
        # processes the data as a flat longitude-latitude pair
        get_polygon='-',
        get_fill_color=[0, 0, 0, 20]
    )
    
    geojson = pydeck.Layer(
        'GeoJsonLayer',
        DATA_URL,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation='properties.valuePerSqm / 20',
        get_fill_color='[255, 255, properties.growth * 255]',
        get_line_color=[255, 255, 255],
        pickable=True
    )
    
    r = pydeck.Deck(
        layers=[polygon, geojson],
        initial_view_state=INITIAL_VIEW_STATE)
    
    r.to_html()
        
def test():
    #folium_static(map)
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon']
    )
    
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ), layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position='[lon, lat]',
                radius=20,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            )
            # , pdk.Layer(
            #     'ScatterplotLayer',
            #     data=df,
            #     get_position='[lon, lat]',
            #     get_color='[200, 30, 0, 160]',
            #     get_radius=200,),
            ],
        )
    )

'''For reference

column_layer = pdk.Layer(
    "ColumnLayer",
    data=df,
    get_position=["lng", "lat"],
    get_elevation="price_per_unit_area",
    elevation_scale=100,
    radius=50,
    get_fill_color=["mrt_distance * 10", "mrt_distance", "mrt_distance * 10", 140],
    pickable=True,
    auto_highlight=True,
)
'''
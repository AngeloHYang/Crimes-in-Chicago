'''
    Utils that are related to map creation
'''
import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
from dataAccess import return_dataFrames

def fuck():
    theDataFrame = pd.DataFrame(return_dataFrames("Crime_data"))
    theDataFrame = pd.DataFrame(theDataFrame.groupby(theDataFrame['District']).count()).reset_index()
    theDataFrame = theDataFrame[['District', 'Case Number']].rename(columns={'Case Number': 'Count'})
    extra = pd.DataFrame(return_dataFrames('DistrictToCoordinates_mean'))
    theDataFrame = pd.merge(theDataFrame, extra, on='District')
    theDataFrame['Elevation'] = theDataFrame['Count'].div(1000)
    return theDataFrame

def getColorValue(theValue, lower, upper):
    #st.write(theValue)
    a = [128,128,255]
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
        get_fill_color=getColorValue(dataFrame['Elevation'].to_list()[0], lower, upper)
    )
    return theLayer
    

def drawMap(dataFrame, location_mark):
    #dataFrame.rename(columns={"Longitude": "lon", "Latitude": "lat"}, inplace=True)
    #ataFrame.drop(['District'], inplace=True, axis=1)
    st.write(fuck())
    
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
            latitude=41.7785,
            longitude=-87.7152,
            zoom=14,
            pitch=50,
        ), layers=[
            getLayer(row, 1, 100) for index, row in fuck().iterrows()
            # , pdk.Layer(
            #     'ScatterplotLayer',
            #     data=fuck(),
            #     get_position='[Longitude, Latitude]',
            #     get_color='[200, 30, 0, 160]',
            #     get_radius=200,),
            ],
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
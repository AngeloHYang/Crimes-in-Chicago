'''
    Functions related to data accessing, such as saving and reading predict models, necessary csv files
'''

import streamlit as st
import os


## Data File Related
DataPath = "../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/"
DataFileName = [
    'Chicago_Crimes_2001_to_2004.csv', 
    'Chicago_Crimes_2005_to_2007.csv', 
    'Chicago_Crimes_2008_to_2011.csv', 
    'Chicago_Crimes_2012_to_2017.csv'
]

def check_dataFiles():
    FileExist = True
    if os.path.exists(DataPath):
        for i in DataFileName:
            fullDataFileName = DataPath + i
            if os.path.exists(fullDataFileName) == False:
                FileExist = False
                break
    return FileExist


## Comoonly used DataFrame Related
def check_DataFrames():
    return False

def create_DataFrames():
    return check_DataFrames()


## Prediction Model Related
def check_models():
    return False

def create_models():
    return check_models()
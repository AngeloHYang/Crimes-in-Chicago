'''
    Utilities that may come handy
'''
import streamlit as st
import os

# When you want to delete a bunch of keys from 
def batch_delele_from_sessionState(stringOrList):
    if isinstance(stringOrList, str):
        if stringOrList in st.session_state:
            del st.session_state[stringOrList]
    elif isinstance(stringOrList, list):
        for i in stringOrList:
            if i in st.session_state:
                del st.session_state[i]
    else:
        print('Delete from session_state error')
        
def checkFiles(pathString, fileNameList, fileNameExtension=""):
    if not os.path.exists(pathString) or not os.path.isdir(pathString):
        return False
        
    Exist = True
    for i in fileNameList:
        filename = i + fileNameExtension
        if not os.path.exists(pathString + filename) or not os.path.isfile(pathString + filename):
            Exist = False
            break
    return Exist
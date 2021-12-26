import streamlit as st
import gettext
from init import init_app

init_app()

st.sidebar.radio(("Navigation Bar"),("Overview", "Check by the city", "Check by street name", "Check by block name"))

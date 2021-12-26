import streamlit as st
import time
from init import init_app


init_app()

st.write("# Hello, Chicago")
st.write("> They had it coming, they had it coming\n\n> They had it coming all along!\n\n> 'Cause if they used us, and they abused us\n\n> How could they tell us that we were wrong?")

with st.spinner("Please wait..."):
    time.sleep(1)

st.sidebar.write("Wow")
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)
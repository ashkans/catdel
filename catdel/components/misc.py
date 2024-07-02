import streamlit as st
from catdel import process
import io
from catdel import grid_processors
from catdel.state_manager import StateManager


def file_uploader_on_change():
    StateManager.get_instance(reset=True)
    

def file_uploader():
    sm = StateManager.get_instance()
    st.write("## Digital Elevation Map")
    uploaded_file = st.file_uploader("Upload a DEM file", type=["tif"], key='file_upload', on_change=file_uploader_on_change)
    return sm.add_states(uploaded_file=uploaded_file)




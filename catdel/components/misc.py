import streamlit as st
from catdel import process
import io
from catdel import grid_processors
from catdel.state_manager import StateManager


def file_uploader_on_change():
    StateManager.get_instance(reset=True)
    


def file_uploader():
    sm = StateManager.get_instance()
    config = sm.config

    st.write("## Digital Elevation Map")
    uploaded_file = st.file_uploader("Upload a DEM file", type=["tif"], key='file_upload', on_change=file_uploader_on_change)
    
    if uploaded_file:
        if not sm.demUploaded:
            # Read the file from the uploaded file buffer
            file_buffer = io.BytesIO(uploaded_file.getvalue())
            grid, dem = process.load_grid_and_data(file_buffer, config.proj.pyproj)
            sm.add_states(grid=grid, dem=dem)
            sm.demUploaded=True




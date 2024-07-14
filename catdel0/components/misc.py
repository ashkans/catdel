import streamlit as st
from catdel import process
import io
from catdel import grid_processors
from catdel.state_manager import StateManager
from catdel import db
from catdel import object_store

def file_uploader_on_change():
    StateManager.get_instance(reset=True)
    
    

def file_uploader():
    sm = StateManager.get_instance()
    st.write("### Upload a DEM file")
    uploaded_file = st.file_uploader("uploader",
    type=["tif"],
    key='file_upload',
    on_change=file_uploader_on_change,
    accept_multiple_files=False,
    label_visibility='collapsed',
    )
    sm.add_states(uploaded_file=uploaded_file)
    
    if uploaded_file:
        if not sm.file_saved:
            if st.config.get_option('server.runOnSave'):
                object_store.upload_from_bytes(uploaded_file.getvalue())
                sm.file_saved = True
    




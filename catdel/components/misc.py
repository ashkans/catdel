import streamlit as st
from catdel import process
import io
from catdel import grid_processors
from catdel.state_manager import StateManager


def file_uploader_on_change():
    StateManager.get_instance(reset=True)
    

def file_uploader():
    sm = StateManager.get_instance()
    st.write("## Upload a DEM file")
    uploaded_file = st.file_uploader("uploader",
     type=["tif"],
     key='file_upload',
     on_change=file_uploader_on_change,
     accept_multiple_files=False,
     label_visibility='collapsed')
    return sm.add_states(uploaded_file=uploaded_file)




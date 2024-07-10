
from catdel.state_manager import StateManager
from catdel import process
import streamlit as st

from catdel import db



def delineate():
        
        sm = StateManager.get_instance()
        process_button_disabled = False # sm.outlet_lat is None
        if process_button_disabled:
            process_button_name = 'Please select the outlet location on map.'
        else:
            process_button_name = 'Delineate!'

        st.button(process_button_name, on_click=process.run_deliniation, type='primary', use_container_width=True, disabled=process_button_disabled)
        
def download_catchment():
        def handel_click():
            db.log('download_catchment', 'na')        
        sm = StateManager.get_instance()
        if sm.delin is not None:

            buffer = process.buffer_catchment_geojson()

            st.download_button(
                label="Download Catchment Shape as GeoJSON",
                data=buffer,
                file_name="catchment_shape.geojson",
                mime="application/geo+json",
                use_container_width=True,
                on_click=handel_click
            )


def download_streams():
        def handel_click():
            db.log('download_streams', 'na')        
        sm = StateManager.get_instance()
        if sm.delin is not None:

            buffer = process.buffer_stream_geojson()

            st.download_button(
                label="Download Stream Shape as GeoJSON",
                data=buffer,
                file_name="stream_shape.geojson",
                mime="application/geo+json",
                use_container_width=True,
                on_click=handel_click
            )


def add_sample_data_download():
    def handel_click():
        db.log('add_sample_data_download', 'na')
        
    with open("sample_data/sample_dem.tif", "rb") as file:
        st.sidebar.download_button(
            label='📥 Download Sample DEM File',
            data=file,
            file_name='sample_dem.tif',
            mime='image/tiff',  # Add the mime type here
            use_container_width=True,
            on_click=handel_click
        )

        


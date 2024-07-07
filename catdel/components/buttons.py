
from catdel.state_manager import StateManager
from catdel import process
import streamlit as st



def delineate():
        sm = StateManager.get_instance()
        process_button_disabled = False # sm.outlet_lat is None
        if process_button_disabled:
            process_button_name = 'Please select the outlet location on map.'
        else:
            process_button_name = 'Delineate!'

        st.button(process_button_name, on_click=process.run_deliniation, type='primary', use_container_width=True, disabled=process_button_disabled)
        
def download_catchment():
        
        sm = StateManager.get_instance()
        if sm.delin is not None:

            buffer = process.buffer_catchment_geojson()

            st.download_button(
                label="Download Catchment Shape as GeoJSON",
                data=buffer,
                file_name="catchment_shape.geojson",
                mime="application/geo+json",
                use_container_width=True
            )


def download_streams():
        
        sm = StateManager.get_instance()
        if sm.delin is not None:

            buffer = process.buffer_stream_geojson()

            st.download_button(
                label="Download Stream Shape as GeoJSON",
                data=buffer,
                file_name="stream_shape.geojson",
                mime="application/geo+json",
                use_container_width=True
            )


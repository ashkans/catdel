import streamlit as st
from catdel.components.map import Map
from catdel.process import dem_processing as dp
from catdel.state_manager import StateManager
from io import BytesIO
from catdel.database import database as db

sm = StateManager.get_instance()


def buffer_geojson(dataframe):
    """
    Convert a GeoDataFrame to a GeoJSON buffer.
    
    Parameters:
    dataframe (GeoDataFrame): The GeoDataFrame to convert.
    
    Returns:
    BytesIO: A buffer containing the GeoJSON data.
    """
    buffer = BytesIO()
    geojson = dataframe.to_json()
    buffer.write(geojson.encode('utf-8'))
    buffer.seek(0)
    return buffer

def buffer_stream_geojson():
    gdf = sm.delin_results['branches']
    return buffer_geojson(gdf)

def buffer_catchment_geojson():
    gdf = sm.delin_results['catchment_shape']
    return buffer_geojson(gdf)



def _delin(loc):
    return dp.delin(sm.dem, sm.grid, sm.config.acc_thr, sm.config.snap_thr, loc, dst_crs=sm.config.proj.dst_crs)    


def handel_delin_button():
    db.log('Delin button is clicked.', 'na')
    sm.delin_results = _delin(sm.outlet_geo)
    sm.catchment_plotted=False # need to replot as a new delin is happened
    map = Map()
    map.build_map() # to remove all old catchments
    map.add_catchment_boundary(sm.delin_results['catchment_shape'])
    map.add_catchment_branches(sm.delin_results['branches'])

def handel_download_catch():
    db.log('Download catchment button is clicked.', 'na')


def handel_download_stream():
    db.log('Download stream button is clicked.', 'na')

    
def delin_button():
    if sm.dem is not None:
        st.button('Delin',use_container_width=True, on_click=handel_delin_button)


def download_catch_button():
    if sm.delin_results is not None:
        buffer = buffer_stream_geojson()
        st.download_button('Download Catchment',
                            data=buffer,
                            file_name="catchment.geojson",
                            mime="application/geo+json",
                            use_container_width=True,
                            on_click=handel_download_catch)    


def download_stream_button():
    if sm.delin_results is not None:
        buffer = buffer_stream_geojson()
        st.download_button('Download Stream',
                            data=buffer,
                            file_name="stream.geojson",
                            mime="application/geo+json",
                            use_container_width=True,
                            on_click=handel_download_stream)
    

def download_sample_data():
    def handel_click():
        db.log('download_sample_data', 'na')
        
        
    with open("sample_data/sample_dem.tif", "rb") as file:
        st.sidebar.download_button(
            label='📥 Download Sample DEM File',
            data=file,
            file_name='sample_dem.tif',
            mime='image/tiff',  # Add the mime type here
            use_container_width=True,
            on_click=handel_click
        )




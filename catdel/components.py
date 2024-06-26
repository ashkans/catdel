import streamlit as st
from catdel import process

def options(grid):        
        lon_default, lat_default = process.get_center(grid)
        lat = st.number_input(label='Latitude',
                                   value=lat_default,
                                   on_change=None)
        lon = st.number_input(label='Longitude',
                                   value=lon_default,
                                   on_change=None)
        acc_thr = st.number_input(label='Accumulation threshold',
                                   value=1000,
                                   on_change=None)
        return {"lat":lat, "lon":lon, "acc_thr":acc_thr}

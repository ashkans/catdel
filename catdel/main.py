import streamlit as st
from catdel.state_manager import StateManager
from catdel.add_ga import inject_ga_if_on_server
from catdel.components.dem_uploader import DemUploader
from catdel.components.map import Map
from catdel.components import buttons
from catdel.helpers import load_dem_and_grid
from catdel.process import dem_processing as dp
import numpy as np
from catdel.components import feature_request

sm = StateManager.get_instance()


# initialize
inject_ga_if_on_server()

st.set_page_config('CatDel',**sm.config.page_config) # should go to config
    

def main():

    # fileloader
    du = DemUploader()
    du()
    load_dem_and_grid()

    # map
    m = Map()
    m()
    
    # delin cat
    buttons.delin_button() # handel no data yet for thiss
    buttons.download_catch_button()
    buttons.download_stream_button()

    with st.sidebar:
        feature_request.expander()
        buttons.download_sample_data()


    # next is to find subcatchments.
        
        

    
    sm.outlet
    sm.delin_results
    st.write(sm.map_outputs)
    sm.catchment_plotted 


if __name__ == '__main__':
    main()


import streamlit as st
from catdel import components
from catdel import process
from streamlit_folium import st_folium

from catdel.state_manager import StateManager


def add_all_streams():
    sm = StateManager.get_instance()
    config=sm.config
    dem, grid = sm.get_states('dem', 'grid')
    allStreams =  process.all_streams(dem, grid, config)
    sm.add_states(allStreams=allStreams)
    sm.allStreamsAdded = False
    sm.allStreamsCalculated = True



def run_deliniation():
    sm = StateManager.get_instance()
    config=sm.config
    dem, grid = sm.get_states('dem', 'grid')
    out = process.delin(dem, grid, config)
    sm.add_states(delin=out)
    sm.streamsAdded = False
    sm.catchmentAdded = False
    sm.outletAdded= False
    sm.needsRender = True
    sm.boundaryAdded=False
    sm.map=None
    sm.allStreamsAdded=False
    
def render_map_if_needed():
    sm = StateManager.get_instance()
    if sm.needsRender:
        _ = sm.map
        sm.needsRender = False
    



def get_map():
    sm = StateManager.get_instance()
    
    if not sm.map:
        components.folium_map.folium_map()
        components.folium_map.last_clicked_holder()
        sm.needsRender = True
    
    if not sm.boundaryAdded:
        components.folium_map.add_grid_boundary()
        sm.boundaryAdded = True
        sm.needsRender = True

    if sm.allStreamsCalculated and not sm.allStreamsAdded:
        components.folium_map.add_allStreams()
        sm.allStreamsAdded = True
        sm.needsRender = True

    if sm.delin:
        if sm.showStreams and not sm.streamsAdded:
            components.folium_map.add_riversystem()
            components.folium_map.add_outlet()
            sm.streamsAdded = True
            sm.needsRender = True


        if sm.showOutlet and not sm.outletAdded:
            components.folium_map.add_outlet()
            sm.outletAdded = True
            sm.needsRender = True


        if sm.showCatchment and not sm.catchmentAdded:
            components.folium_map.add_catchment()
            sm.catchmentAdded=True
            sm.needsRender= True
    

    render_map_if_needed()
    return sm.map


def main():
    sm = StateManager.get_instance()
    config = sm.config

    file_buffer = components.misc.file_uploader()


    if sm.demUploaded:
        
        st.button('Process', on_click=run_deliniation, type='primary', use_container_width=True, disabled=False)
        st.button('Add all streams', on_click=add_all_streams, type='primary', use_container_width=True, disabled=False)
        m = get_map()
        
        output = st_folium(m, width=config.map_width, height=config.map_height, returned_objects=None, render=False)
        components.folium_map.last_clicked_recorder(output)
        
    st.write(st.session_state)



        

if __name__ == '__main__':
    main()

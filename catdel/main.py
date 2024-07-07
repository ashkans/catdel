import folium.raster_layers
import streamlit as st



from catdel import components
from catdel import process
from streamlit_folium import st_folium
from catdel.state_manager import StateManager

sm = StateManager.get_instance()
st.set_page_config('CatDel',**sm.config.page_config) # should go to config




# only load Google analytics on server
if st.config.get_option('server.runOnSave'):
    from catdel import add_ga
    add_ga.inject_ga()


def main():
    
    config = sm.config
    
    with st.expander('', expanded=sm.dem is None, icon=':material/upload:'):
        components.misc.file_uploader()

    
    with st.spinner('Reading Grid and DEM...'):
        process.read_grid_and_dem()
    with st.spinner('Adding all streams...'):
        process.add_all_streams() 

    
    if sm.dem is not None:
        
        m = components.folium_map.get_map()





        with st.container(height=int(config.map_height*1.3)):
            
            sm.map_outputs = st_folium(m,
                            width=config.map_width,
                            height=config.map_height,
                            returned_objects=['last_clicked'],
                            render=False,
                            use_container_width=True)
            if not sm.outlet:
                st.write('### Select the location of the outlet on the map')
            
        

        c1,c2,c3 = st.columns([0.33, 0.33, 0.33])
        with c1:
            components.buttons.delineate()
            
        with c2:
            components.buttons.download_catchment()

        with c3: 
            components.buttons.download_streams()

    with st.sidebar:
        components.feature_request.modal()

    if not st.config.get_option('server.runOnSave'):
        #st.write(st.session_state)
        pass

    else:
        pass

    #components.footer.footer()


if __name__ == '__main__':
    main()

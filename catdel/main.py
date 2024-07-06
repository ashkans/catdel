import streamlit as st
from catdel import components
from catdel import process
from streamlit_folium import st_folium

from catdel.state_manager import StateManager


def main():
    st.set_page_config(layout="wide")
    sm = StateManager.get_instance()
    config = sm.config
    components.misc.file_uploader()
    
    with st.spinner('Reading Grid and DEM...'):
        process.read_grid_and_dem()
    with st.spinner('Adding all streams...'):
        process.add_all_streams()

    if sm.dem is not None:

        components.buttons.delineate()
        components.buttons.download_catchment()
        m = components.folium_map.get_map()

        output = st_folium(m,
                           width=config.map_width,
                           height=config.map_height,
                           returned_objects=['last_clicked'],
                           render=False,
                           use_container_width=True)
        components.folium_map.last_clicked_recorder(output)

    
    components.feature_request.modal()
    if not st.config.get_option('server.runOnSave'):
        #st.write(st.session_state)
        pass
    else:
        pass


    
    #components.footer.footer()

if __name__ == '__main__':
    main()

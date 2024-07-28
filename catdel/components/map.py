from catdel.components.base_component import BaseComponent
import streamlit as st
from catdel.state_manager import StateManager
import folium
from catdel.process.utils import get_grid_center_geo
from streamlit_folium import st_folium

sm = StateManager.get_instance()



class Map(BaseComponent):
    '''
    this class should have a build_base_map
    add shape file 
    add point
    retrive data - a function that can be called by others so this returns last point clicked.
    '''

    def call(self):
        m = self.get_map()
        config = sm.config

        if isinstance(m, folium.Map):
            sm.map_outputs = st_folium(m,
                            width=config.map_width,
                            height=config.map_height,
                            returned_objects=['last_clicked'],
                            render=False,
                            use_container_width=True)        

    
    
    def get_map(self):
        '''
        checks if the map is stored in sm, if not build if stored return it.
        '''
        if not sm.map:
            self.build_map()

        return sm.map



    def build_map(self):
        '''
        this make the base map and adds components.  
        '''
        m = self.build_base_map()
        sm.map=m
        


    def build_base_map(self):
        '''
        this makes the map and store it in sm
        '''
        
        if sm.grid is not None:
            grid = sm.grid
            config = sm.config

            geographic_center = get_grid_center_geo(grid, config.proj) # TODO should go to the initiale process and saved as state
            m = folium.Map(location=geographic_center,
            zoom_start=config.zoom_start,
            crs=config.proj.folium_proj,
            max_zoom=config.max_zoom,
            min_zoom=config.min_zoom,
            prefer_canvas=True)
            return m
        else:
            # handel no grid call
            return 'No grid file yet'
            






    





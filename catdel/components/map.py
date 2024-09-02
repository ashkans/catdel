from catdel.components.base_component import BaseComponent
from catdel.state_manager import StateManager
import folium
from catdel.process.utils import get_grid_center_geo, get_grid_bounds_geo
from streamlit_folium import st_folium
from catdel.folium_elements.outlet_selector import OutletSelector
import numpy as np


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



        if isinstance(m, folium.Map):
            
            sm.map_outputs = st_folium(m,
                            width=sm.config.map_width,
                            height=sm.config.map_height,
                            returned_objects=['last_clicked'],
                            render=False,
                            use_container_width=True,
                            #feature_group_to_add=sm.catchment_boundaries_fg
                            )
            
    
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
        center = get_grid_center_geo(sm.grid, sm.config.proj)  if sm.grid is not None else sm.config.coord_start
        sm.map = self.build_base_map(center)
        
        # this is making a boundary of the dem.
        if sm.config.show_dem_boundary and sm.grid is not None:
            geographic_bounds = get_grid_bounds_geo(sm.grid, sm.config.proj)
            self.add_boundary(geographic_bounds)

        if sm.all_branches is not None:
            self.add_all_rivers()
            sm.all_rivers_plotted = True   
        
        

    @staticmethod
    def add_boundary(geographic_bounds):
        folium.Rectangle(
        bounds=geographic_bounds,
        color='blue',
        weight=2,
        fill=False,
        fill_color='blue',
        fill_opacity=0.2,
        ).add_to(sm.map)
        
        
            

    def build_base_map(self, center):
        '''
        this makes the map and store it in sm
        '''
        m = folium.Map(location=center,
        zoom_start=sm.config.zoom_start,
        crs=sm.config.proj.folium_proj,
        max_zoom=sm.config.max_zoom,
        min_zoom=sm.config.min_zoom,
        prefer_canvas=True,)
        #png_enabled=True,
        #no_touch=True)
        OutletSelector().add_to(m)
        return m
    
    
    @staticmethod
    def add_polyline_geo(geo_line, **kwargs):
        folium.PolyLine(locations=geo_line, **kwargs).add_to(sm.map)

    
    def add_polyline_proj(self, line, **kwargs):
        geo_line = sm.config.proj.transform_array_to_geo(line)    
        self.add_polyline_geo(geo_line, **kwargs)

    def add_catchment_boundary(self, gdf):
        # Add polygons from the GeoDataFrame to the map
        if not sm.catchment_plotted and sm.delin_results is not None:

            for _, row in gdf.iterrows():
                
                locations = sm.config.proj.transform_array_to_geo([[point[0], point[1]] for point in row['geometry'].exterior.coords])
                
                folium.vector_layers.Polygon(
                    locations=locations,
                    color='red',
                    fill=True,
                    fill_color='red',  # Fill color
                    fill_opacity=0.3,  # Fill opacity
                    weight=2  # Outline weight
                ).add_to(sm.map)
            
            sm.catchment_plotted = True    

            
    def plot_river_gdf(self, gdf, **kwargs):
        for _, branch in gdf.iterrows():
            line = np.asarray(branch['geometry'].coords) 
            self.add_polyline_proj(line, **kwargs)            
                    
    def add_catchment_branches(self, gdf):
        self.plot_river_gdf(gdf,weight=3,)


    def add_all_rivers(self, **kwargs):
        self.plot_river_gdf(sm.all_branches, weight=2, color="green")
       
            


    





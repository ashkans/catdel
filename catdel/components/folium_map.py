from catdel.grid_processors import get_grid_center_geo, get_grid_bounds_geo
import folium
import streamlit as st
import numpy as np
from catdel.state_manager import StateManager
from shapely.geometry import shape
import geopandas as gpd

def last_clicked_holder():
    sm = StateManager.get_instance()
    m = sm.map
    m.add_child(folium.LatLngPopup())

def last_clicked_recorder(output):
    sm = StateManager.get_instance()

    lc = output['last_clicked']
    if lc:
        sm.outlet_lat = lc['lat']
        sm.outlet_lng = lc['lng']
        


def add_outlet():
    sm = StateManager.get_instance()
    m = sm.map
    proj = sm.config.proj
    loc = sm.outlet_lat, sm.outlet_lng
    
    folium.Marker(loc).add_to(m)
    

def folium_map():
    sm = StateManager.get_instance()
    grid = sm.get_state('grid')
    config = sm.config

    geographic_center = get_grid_center_geo(grid, config.proj)
    m = folium.Map(location=geographic_center, zoom_start=config.zoom_start, crs=config.proj.folium_proj, max_zoom=config.max_zoom, min_zoom=config.min_zoom)
    sm.add_states(map=m)


def add_catchment():
    sm = StateManager.get_instance()
    config = sm.config
    catchment = sm.delin['catchment_shape']
    grid = sm.grid
    m=sm.map

    tolerance=1
    geoms = [shape(s[0]).simplify(tolerance)  for s in catchment]
    gdf = gpd.GeoDataFrame({'geometry': geoms}, crs=config.proj.dst_crs)
    
    # Add polygons from the GeoDataFrame to the map
    for _, row in gdf.iterrows():
        locations = config.proj.transform_array_to_geo([[point[0], point[1]] for point in row['geometry'].exterior.coords])
        
        folium.vector_layers.Polygon(
            locations=locations,
            color='red',
            fill=True,
            fill_color='red',  # Fill color
            fill_opacity=0.3,  # Fill opacity
            weight=2  # Outline weight
        ).add_to(m)

        
    


def add_allStreams():
    sm = StateManager.get_instance()
    branches = sm.allStreams
    config = sm.config
    m=sm.map

    for branch in branches['features']:
        line = np.asarray(branch['geometry']['coordinates']) 
        geo_line = config.proj.transform_array_to_geo(line)         
        folium.PolyLine(locations=geo_line,weight=1, color='gray').add_to(m)
    
        
def add_riversystem():
    sm = StateManager.get_instance()
    branches = sm.delin['branches']
    config = sm.config
    m=sm.map

    for branch in branches['features']:
        line = np.asarray(branch['geometry']['coordinates']) 
        geo_line = config.proj.transform_array_to_geo(line)         
        folium.PolyLine(locations=geo_line,weight=3).add_to(m)
    
        
        

def add_grid_boundary():
    sm = StateManager.get_instance()
    grid = sm.get_state('grid')
    config = sm.config
    m = sm.map

    geographic_bounds = get_grid_bounds_geo(grid, config.proj)
    folium.Rectangle(
    bounds=geographic_bounds,
    color='blue',
    weight=2,
    fill=False,
    fill_color='blue',
    fill_opacity=0.2,
    ).add_to(m)
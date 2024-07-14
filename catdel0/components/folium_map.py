from catdel.grid_processors import get_grid_center_geo, get_grid_bounds_geo
import folium
import streamlit as st
import numpy as np
from catdel.state_manager import StateManager
from catdel import components
from catdel import process
import folium
import numpy as np
from catdel.grid_processors import get_grid_center_geo, get_grid_bounds_geo, get_grid_bounds
sm = StateManager.get_instance()        

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
    
    m = sm.map
    
    loc = sm.outlet
    
    folium.Marker(loc).add_to(m)


def add_raster(raster, name = None, opacity=0.6, interactive=True, cross_origin=False, zindex=1000, **kwargs):
        geographic_bounds = get_grid_bounds_geo(sm.grid, sm.config.proj)
        img = folium.raster_layers.ImageOverlay(
        name=name,
        image=np.where(raster, raster, np.nan),
        bounds=geographic_bounds,
        opacity=opacity,
        interactive=interactive,
        cross_origin=cross_origin,
        zindex=zindex,
        **kwargs
        )
        img.add_to(sm.map)


def folium_map():
    sm = StateManager.get_instance()
    grid = sm.get_state('grid')
    config = sm.config

    geographic_center = get_grid_center_geo(grid, config.proj) # TODO should go to the initiale process and saved as state
    m = folium.Map(location=geographic_center,
     zoom_start=config.zoom_start,
     crs=config.proj.folium_proj,
     max_zoom=config.max_zoom,
     min_zoom=config.min_zoom,
     prefer_canvas=True)
    sm.add_states(map=m)



def add_catchment():
    sm = StateManager.get_instance()
    config = sm.config
    gdf = process.convert_catchment_to_gdf()
    grid = sm.grid

    
    m = sm.map
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
        folium.PolyLine(locations=geo_line,weight=2, color='gray').add_to(m)
    
        
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



    
def render_map_if_needed():
    sm = StateManager.get_instance()
    if sm.needsRender:
        _ = sm.map
        sm.needsRender = False
    



def get_map():
    
    sm = StateManager.get_instance()
    
    if not sm.map:
        
        folium_map()
        last_clicked_holder()
        components.plugins.add_plugins()
        sm.needsRender = True
    
    if not sm.boundaryAdded:
        add_grid_boundary()
        sm.boundaryAdded = True
        sm.needsRender = True

    if sm.allStreamsCalculated and not sm.allStreamsAdded:
        add_allStreams()
        sm.allStreamsAdded = True
        sm.needsRender = True

    if sm.delin:
        if sm.showStreams and not sm.streamsAdded:
            add_riversystem()
            add_outlet()
            sm.streamsAdded = True
            sm.needsRender = True


        if sm.showOutlet and not sm.outletAdded:
            add_outlet()
            sm.outletAdded = True
            sm.needsRender = True


        if sm.showCatchment and not sm.catchmentAdded:
            add_catchment()
            sm.catchmentAdded=True
            sm.needsRender= True
    


    #render_map_if_needed()
    

    return sm.map
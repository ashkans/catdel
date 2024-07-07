from typing import Union, Tuple
import io
from pysheds.grid import Grid
from pysheds.sview import Raster
import streamlit as st
import numpy as np
from catdel.state_manager import StateManager

from shapely.geometry import shape, mapping
from shapely.geometry import LineString, Polygon, MultiPolygon

from io import BytesIO
import geopandas as gpd
sm = StateManager.get_instance()
dirmap = (64, 128, 1, 2, 4, 8, 16, 32)

def load_grid_and_data(fn: Union[str, io.BytesIO], pyproj:str) -> Tuple[Grid, Raster]:
    """
    Loads a grid and associated data from a raster file.

    Args:
    fn (Union[str, io.BytesIO]): The file name or a BytesIO object of the raster file.

    Returns:
    Tuple[Grid, Data]: A tuple containing the grid and its associated data.
    """
    grid = Grid()
    data = grid.read_raster(fn)
    data = data.to_crs(pyproj)
    grid.viewfinder = data.viewfinder
    return grid, data


def simplify_geometry(geometry, tolerance):
    geom = shape(geometry)
    if isinstance(geom, (LineString, Polygon, MultiPolygon)):
        simplified_geom = geom.simplify(tolerance, preserve_topology=True)
        return mapping(simplified_geom)
    return geometry  # Return as is if it's not a LineString or Polygon


def simplify_geojson_collection(geojson_obj, tolerance):
    if geojson_obj['type'] == 'FeatureCollection':
        for feature in geojson_obj['features']:
            feature['geometry'] = simplify_geometry(feature['geometry'], tolerance)
    elif geojson_obj['type'] == 'Feature':
        geojson_obj['geometry'] = simplify_geometry(geojson_obj['geometry'], tolerance)
    else:
        geojson_obj = simplify_geometry(geojson_obj, tolerance)
    return geojson_obj


def delin_preprocess(dem, grid):
    pit_filled_dem = grid.fill_pits(dem)
    # Fill depressions in DEM
    flooded_dem = grid.fill_depressions(pit_filled_dem)
    # Resolve flats in DEM
    inflated_dem = grid.resolve_flats(flooded_dem)
    
    fdir = grid.flowdir(inflated_dem, dirmap=dirmap)
    acc = grid.accumulation(fdir, dirmap=dirmap)

    return acc, fdir

def all_streams(dem, grid, config):
    acc, fdir = delin_preprocess(dem, grid)
    branches = grid.extract_river_network(fdir,
                                            acc > config.acc_thr,
                                            dirmap=dirmap)
    branches = simplify_geojson_collection(branches, 5000)
    return branches

def delin(dem, grid, config):
    # Delineate a catchment
    # ---------------------
    # Fill pits in DEM
    acc, fdir = delin_preprocess(dem, grid)

    # Snap pour point to high accumulation cell
    lat, lng = sm.outlet
    x, y = config.proj.transform_from_geo(lat, lng)
    
    lat_snap, lng_snap = grid.snap_to_mask(acc > config.snap_thr, (x, y))

    sm.outlet_snap = (lat_snap, lng_snap)
    

    # Delineate the catchment
    catch = grid.catchment(x=lat_snap,
                           y=lng_snap,
                           fdir=fdir,
                           dirmap=dirmap,
                           xytype='coordinate')

    
    
    grid.clip_to(catch)
    clipped_catch = grid.view(catch)

    # Create view
    catch_view = grid.view(clipped_catch, dtype=np.uint8)

    # Create a vector representation of the catchment mask
    catchment_shape = list(grid.polygonize(catch_view))


    branches = grid.extract_river_network(fdir,
                                            acc > config.acc_thr,
                                            dirmap=dirmap)
    


    branches = simplify_geojson_collection(branches, 0.001)

    out = {'catch': catch, 'branches':branches, 'catchment_shape': catchment_shape}

    grid.viewfinder = dem.viewfinder
    return out



def add_all_streams():
    sm = StateManager.get_instance()
    if not sm.allStreamsCalculated and sm.dem is not None:
        config=sm.config
        dem, grid = sm.get_states('dem', 'grid')
        allStreams =  all_streams(dem, grid, config)
        sm.add_states(allStreams=allStreams)
        sm.allStreamsAdded = False
        sm.allStreamsCalculated = True


def run_deliniation():

    sm = StateManager.get_instance()

    if sm.map_outputs is None or sm.map_outputs['last_clicked'] is None:
        st.toast('Please select the catchment outlet first.') 

    else:

        config=sm.config
        dem, grid = sm.get_states('dem', 'grid')
        out = delin(dem, grid, config)
        sm.add_states(delin=out)
        sm.streamsAdded = False
        sm.catchmentAdded = False
        sm.outletAdded= False
        sm.needsRender = True
        sm.boundaryAdded=False
        sm.map=None
        sm.allStreamsAdded=False


def read_grid_and_dem():
    sm = StateManager.get_instance()
    config = sm.config
    if sm.uploaded_file and sm.dem is None:
        # Read the file from the uploaded file buffer
        file_buffer = io.BytesIO(sm.uploaded_file.getvalue())
        grid, dem = load_grid_and_data(file_buffer, config.proj.pyproj)
        sm.add_states(grid=grid, dem=dem)


def convert_streams_to_gdf():
    sm = StateManager.get_instance()
    branches = sm.delin['branches']
    gdf = gpd.GeoDataFrame.from_features(branches, crs=sm.config.dst_crs)
    return gdf



def convert_catchment_to_gdf():
    sm = StateManager.get_instance()
    config = sm.config
    catchment = sm.delin['catchment_shape']

    tolerance=1
    geoms = [shape(s[0]).simplify(tolerance)  for s in catchment]
    gdf = gpd.GeoDataFrame({'geometry': geoms}, crs=config.proj.dst_crs)
    
    return gdf


def buffer_stream_geojson():
    # Convert DataFrame to CSV and store in buffer
    buffer = BytesIO()
    gdf = convert_streams_to_gdf()
    #gdf.to_file(buffer, index=False)
    
    
    # Convert GeoDataFrame to GeoJSON
    geojson = gdf.to_json()

    # Create a buffer and write GeoJSON to it
    
    buffer.write(geojson.encode('utf-8'))
    buffer.seek(0)

    return buffer

def buffer_catchment_geojson():
    # Convert DataFrame to CSV and store in buffer
    buffer = BytesIO()
    gdf = convert_catchment_to_gdf()
    #gdf.to_file(buffer, index=False)
    
    # Convert GeoDataFrame to GeoJSON
    geojson = gdf.to_json()

    # Create a buffer and write GeoJSON to it
    
    buffer.write(geojson.encode('utf-8'))
    buffer.seek(0)

    return buffer
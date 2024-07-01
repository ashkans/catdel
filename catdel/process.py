from typing import Union, Tuple
import io
from pysheds.grid import Grid
from pysheds.sview import Raster
from catdel.config import Config
import streamlit as st
import numpy as np
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

import geojson
from shapely.geometry import shape, mapping
from shapely.geometry import LineString, Polygon, MultiPolygon
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
    branches = simplify_geojson_collection(branches, 1)
    return branches

def delin(dem, grid, config):
    # Delineate a catchment
    # ---------------------
    # Fill pits in DEM
    acc, fdir = delin_preprocess(dem, grid)

    # Snap pour point to high accumulation cell
    lat, lng = st.session_state['outlet_lat'], st.session_state['outlet_lng'] 
    x, y = config.proj.transform_from_geo(lat, lng)
    
    lat_snap, lng_snap = grid.snap_to_mask(acc > config.snap_thr, (x, y))

    st.session_state['outlet_lat_snap'] = lat_snap
    st.session_state['outlet_lng_snap'] = lng_snap

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
    catchment_shape = grid.polygonize(catch_view)


    branches = grid.extract_river_network(fdir,
                                            acc > config.acc_thr,
                                            dirmap=dirmap)
    


    branches = simplify_geojson_collection(branches, 0.001)

    out = {'catch': catch, 'branches':branches, 'catchment_shape': catchment_shape}

    grid.viewfinder = dem.viewfinder
    return out




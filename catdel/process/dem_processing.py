from typing import Tuple, Any
from catdel.process import utils
from pysheds.grid import Grid
from pysheds.pview import Raster
import numpy as np

# Default direction map used for flow direction calculations
DIRMAP = (64, 128, 1, 2, 4, 8, 16, 32)

def fill_pits(dem: Raster, grid: Grid) -> Raster:
    """Fill pits in the DEM."""
    return grid.fill_pits(dem)

def fill_depressions(dem: Raster, grid: Grid) -> Raster:
    """Fill depressions in the DEM."""
    return grid.fill_depressions(dem)

def resolve_flats(dem: Raster, grid: Grid) -> Raster:
    """Resolve flats in the DEM."""
    return grid.resolve_flats(dem)

def calculate_flow_accumulation(
    dem: Raster, grid: Grid, dirmap: Tuple[int, ...] = DIRMAP
) -> Tuple[Raster, Raster]:
    """
    Calculate flow direction and accumulation for a given DEM using a specified direction map.
    
    Args:
        dem: Digital elevation model data.
        grid: Grid object providing necessary methods for DEM processing.
        dirmap: Tuple specifying the direction mapping for flow direction calculation.
        
    Returns:
        A tuple containing the accumulation and flow direction grids.
    """
    # Validate inputs
    if not hasattr(grid, 'fill_pits') or not hasattr(grid, 'flowdir'):
        raise ValueError("Grid object must have the required methods.")

    # Process the DEM
    pit_filled_dem = fill_pits(dem, grid)
    flooded_dem = fill_depressions(pit_filled_dem, grid)
    inflated_dem = resolve_flats(flooded_dem, grid)
    
    # Calculate flow direction and accumulation
    fdir = grid.flowdir(inflated_dem, dirmap=dirmap)
    acc = grid.accumulation(fdir, dirmap=dirmap)

    return acc, fdir

def all_streams(dem: Any, grid: Any, acc_thr: Any, dst_crs) -> Any:
    """
    Extract all stream networks from the DEM using flow accumulation and direction.

    Args:
        dem: Digital elevation model data.
        grid: Grid object providing necessary methods for DEM processing.
        config: Configuration object containing threshold values and other settings.
        
    Returns:
        Simplified GeoJSON collection representing river networks.
    """
    # Calculate flow direction and accumulation
    acc, fdir = calculate_flow_accumulation(dem, grid, dirmap=DIRMAP)
    
    # Extract river network based on accumulation threshold
    branches = grid.extract_river_network(
        fdir,
        acc > acc_thr,
        dirmap=DIRMAP
    )



    # Simplify the GeoJSON collection for better performance
    simplified_branches = utils.simplify_geojson_collection(branches, 0.1)
    gdf_simplified_branches = utils.convert_streams_to_gdf(simplified_branches, dst_crs)

    return gdf_simplified_branches



def delin(dem:Raster, grid: Grid, acc_thr:int, snap_thr:int, outlet_loc:tuple[float, ...], dst_crs, simplfy_thr=0.1):
    # Delineate a catchment
    # ---------------------
    # Fill pits in DEM
    acc, fdir = calculate_flow_accumulation(dem, grid)

    # Snap pour point to high accumulation cell
    #lat, lng = sm.outlet
    x, y = outlet_loc #config.proj.transform_from_geo(lat, lng)
    
    lat_snap, lng_snap = grid.snap_to_mask(acc > snap_thr, (x, y))

    # Delineate the catchment
    catch = grid.catchment(x=lat_snap,
                           y=lng_snap,
                           fdir=fdir,
                           dirmap=DIRMAP,
                           xytype='coordinate')
    
    grid.clip_to(catch)
    clipped_catch = grid.view(catch)

    # Create view
    
    catch_view = grid.view(clipped_catch, dtype=np.uint8)

    # Create a vector representation of the catchment mask
    catchment_shape = list(grid.polygonize(catch_view))

    branches = grid.extract_river_network(fdir, acc > acc_thr, dirmap=DIRMAP)

    branches = utils.simplify_geojson_collection(branches, simplfy_thr)
    
    gdf_branches = utils.convert_streams_to_gdf(branches, dst_crs)
    gdf_streams = utils.convert_catchment_to_gdf(catchment_shape, dst_crs)

    out = {'branches':gdf_branches, 'catchment_shape': gdf_streams}

    grid.viewfinder = dem.viewfinder
    return out
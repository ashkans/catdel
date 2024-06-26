from typing import Union, Tuple
import io
from pysheds.grid import Grid
from pysheds.sview import Raster

def load_grid_and_data(fn: Union[str, io.BytesIO]) -> Tuple[Grid, Raster]:
    """
    Loads a grid and associated data from a raster file.

    Args:
    fn (Union[str, io.BytesIO]): The file name or a BytesIO object of the raster file.

    Returns:
    Tuple[Grid, Data]: A tuple containing the grid and its associated data.
    """
    grid = Grid()
    data = grid.read_raster(fn)
    grid.viewfinder = data.viewfinder
    return grid, data


def delin(dem, grid, config=None):
    # Delineate a catchment
    # ---------------------

    # Fill pits in DEM
    pit_filled_dem = grid.fill_pits(dem)
    # Fill depressions in DEM
    flooded_dem = grid.fill_depressions(pit_filled_dem)
    # Resolve flats in DEM
    inflated_dem = grid.resolve_flats(flooded_dem)
    dirmap = (64, 128, 1, 2, 4, 8, 16, 32)
    fdir = grid.flowdir(inflated_dem, dirmap=dirmap)
    acc = grid.accumulation(fdir, dirmap=dirmap)

    # Snap pour point to high accumulation cell
    x_snap, y_snap = grid.snap_to_mask(acc > config['snap_thr'], (config['x'], config['y']))
    config['x_snap'] = x_snap
    config['y_snap'] = y_snap

    # Delineate the catchment
    catch = grid.catchment(x=x_snap,
                           y=y_snap,
                           fdir=fdir,
                           dirmap=dirmap,
                           xytype='coordinate')

    branches = grid.extract_river_network(fdir,
                                            acc > config['acc_thr'],
                                            dirmap=dirmap)
        
    out = {'catch': grid.polygonize(catch), 'branches':branches}

    return out



def get_center(grid):
    e = grid.extent
    return (e[0]+e[1])/2, (e[2]+e[3])/2
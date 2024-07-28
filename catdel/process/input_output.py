from pysheds.grid import Grid
from typing import Union, Tuple
import io
from pysheds.sview import Raster


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
from matplotlib import pylab as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

def add_outlets(config, ax):
    ax.scatter(config['x'], config['y'], marker='o', c='r', s=20)
    ax.scatter(config['snap_x'], config['snap_y'], marker='x', c='r', s=20)


def add_river_system(river_system, ax):

    for branch in river_system['features']:
        line = np.asarray(branch['geometry']['coordinates'])
        ax.plot(line[:, 0], line[:, 1])


def add_raster(data, grid, ax, add_colorbar=True, **kwargs):
    """
    Plots raster data on a given Axes object and optionally adds a colorbar.

    Args:
    data (np.ndarray): The raster data to be displayed.
    grid (Grid): An object containing grid metadata like extent and nodata value.
    ax (Axes): The matplotlib axes object where the data is plotted.
    add_colorbar (bool, optional): If True, adds a colorbar to the plot. Defaults to True.
    **kwargs: Additional keyword arguments passed to imshow.
    """
    
    # Replace grid nodata values with NaN for display
    data = np.where(data == grid.nodata, np.nan, data)

    # Display the data
    im = ax.imshow(data, extent=grid.extent, **kwargs)

    # Optionally add a colorbar
    if add_colorbar:
        add_colorbar_to_plot(ax, im)

def add_colorbar_to_plot(ax, im):
    """
    Adds a colorbar to the plot.

    Args:
    ax (Axes): The matplotlib axes object to which the colorbar will be added.
    im (AxesImage): The image object created by imshow to which the colorbar relates.
    """
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)

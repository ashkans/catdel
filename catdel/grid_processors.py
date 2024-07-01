


def get_grid_bounds(grid):
    return [[grid.extent[0], grid.extent[2]], [grid.extent[1], grid.extent[3]]]

def get_grid_center(grid):
    sw, ne = get_grid_bounds(grid)
    return (sw[0]+ne[0])/2, (sw[1]+ne[1])/2



def get_grid_bounds_geo(grid, projection):
    sw = [grid.extent[0], grid.extent[2]]
    ne = [grid.extent[1], grid.extent[3]]

    return [projection.transform_to_geo(*sw), projection.transform_to_geo(*ne)]    


def get_grid_center_geo(grid, projection):
    sw, ne = get_grid_bounds_geo(grid, projection)
    return (sw[0]+ne[0])/2, (sw[1]+ne[1])/2
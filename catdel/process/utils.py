
from shapely.geometry import shape, mapping
from shapely.geometry import LineString, Polygon, MultiPolygon
import geopandas as gpd


def convert_streams_to_gdf(branches, crs):
    return gpd.GeoDataFrame.from_features(branches, crs=crs)#sm.config.dst_crs)

def convert_catchment_to_gdf(catchment_shape, crs):
    tolerance=1
    geoms = [shape(s[0]).simplify(tolerance)  for s in catchment_shape]
    gdf = gpd.GeoDataFrame({'geometry': geoms}, crs=crs)
    return gdf


def get_grid_bounds(grid):
    return [[grid.extent[0], grid.extent[2]], [grid.extent[1], grid.extent[3]]]

def get_grid_center(grid):
    sw, ne = get_grid_bounds(grid)
    return (sw[0]+ne[0])/2, (sw[1]+ne[1])/2


def get_grid_bounds_geo(grid, projection):
    sw = [grid.extent[0], grid.extent[2]]
    ne = [grid.extent[1], grid.extent[3]]
    return [projection.to_geo(*sw), projection.to_geo(*ne)]    


def get_grid_center_geo(grid, projection):
    sw, ne = get_grid_bounds_geo(grid, projection)
    return (sw[0]+ne[0])/2, (sw[1]+ne[1])/2



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
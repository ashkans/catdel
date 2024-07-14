from pyproj import Proj
from pyproj import Transformer


class Projection():
    def __init__(self, config) -> None:
        self.dst_crs = config.dst_crs
        self.geographic_crs=config.geographic_crs
        self.transformer_to_geo = Transformer.from_crs(config.dst_crs, config.geographic_crs)
        self.transformer_from_geo = Transformer.from_crs(config.geographic_crs, config.dst_crs)


    @property
    def folium_proj(self):
        return self.dst_crs.replace(':', '')
    
    @property
    def pyproj(self):
        return Proj(init=self.dst_crs)
    
    def transform_to_geo(self, x, y):
        return self.transformer_to_geo.transform(x,y)
    
    def transform_from_geo(self, x, y):
        return self.transformer_from_geo.transform(x,y)
        

    def transform_array_to_geo(self, arr):
        return [[*self.transform_to_geo(x, y)] for x, y in arr]
        

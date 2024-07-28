# config_class.py
import yaml
from catdel.projection import Projection


default_config = {
    'snap_thr': 5000,
    'acc_thr': 5000,
    'geographic_crs': 'epsg:4326',
    'dst_crs': 'EPSG:3857',
    'min_zoom': 11,
    'zoom_start': 12,
    'max_zoom': 17,
    'map_width': 700,
    'map_height': 500,
    'map_title': "Folium Map in Streamlit",
    'page_config': {
        'layout': 'wide',
        'page_icon': ':droplet:', #
        'initial_sidebar_state': "expanded",
        'menu_items': {
            'Get Help': None,
            'Report a bug': None,
            'About': "# This is a header. This is an *extremely* cool app!",            
        }
    }
}


class Config:
    def __init__(self):
        self._config = default_config.copy()  # Make a copy of default_config

    def __getattr__(self, name):
        try:
            return self._config[name]
        except KeyError:
            raise AttributeError(f"'Config' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name == '_config':
            super().__setattr__(name, value)
        else:
            self._config[name] = value
    
    def __getitem__(self, name):
        try:
            return self._config[name]
        except KeyError:
            raise AttributeError(f"'Config' object has no attribute '{name}'")
        
    def save(self, file_path):
        with open(file_path, 'w') as f:
            yaml.dump(self._config, f)

    @property
    def proj(self):
        return Projection(self)

    @staticmethod
    def load(file_path):
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)



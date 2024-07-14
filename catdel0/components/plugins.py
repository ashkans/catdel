import folium
import folium.plugins
from catdel.components import folium_map


def add_plugins():
    m = folium_map.get_map()
    #folium.plugins.Draw()
    folium.plugins.Fullscreen().add_to(m)
    folium.plugins.MousePosition().add_to(m)
    

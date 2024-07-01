import streamlit as st
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
import folium
from streamlit_folium import st_folium

# Create a DataFrame with sample data for polygons
data = {
    'name': ['Polygon 1', 'Polygon 2'],
    'coordinates': [
        [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)],  # Square polygon
        [(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)]   # Another square polygon
    ]
}

# Create a GeoDataFrame from the DataFrame
df = pd.DataFrame(data)
gdf = gpd.GeoDataFrame(
    df, 
    geometry=[Polygon(coords) for coords in df['coordinates']],
    crs="EPSG:4326"
)

# Create a folium map centered around the mean coordinates of the GeoDataFrame
m = folium.Map(location=[1.5, 1.5], zoom_start=5)



# Add polygons from the GeoDataFrame to the map
for _, row in gdf.iterrows():
    folium.vector_layers.Polygon(
        locations=[(point[1], point[0]) for point in row['coordinates']],
        popup=row['name']
    ).add_to(m)

# Streamlit app
st.title("Streamlit and Folium with GeoPandas Polygons")
st.write("This is a simple example of using Streamlit and Folium to plot a GeoPandas DataFrame with polygons.")

# Display the map in Streamlit
st_folium(m, width=700, height=500)

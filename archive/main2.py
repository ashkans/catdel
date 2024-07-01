import streamlit as st
import io
import rasterio
from rasterio.errors import RasterioIOError
from rasterio.warp import calculate_default_transform, reproject, Resampling
import folium
from folium import raster_layers
from branca.colormap import LinearColormap
import numpy as np
from streamlit_folium import folium_static
import json
from streamlit_js_eval import get_geolocation

def process_dem(dem_file):
    try:
        mem_file = io.BytesIO(dem_file.getvalue())
        with rasterio.open(mem_file) as src:
            dst_crs = 'EPSG:3857'
            transform, width, height = calculate_default_transform(
                src.crs, dst_crs, src.width, src.height, *src.bounds)
            kwargs = src.meta.copy()
            kwargs.update({
                'crs': dst_crs,
                'transform': transform,
                'width': width,
                'height': height
            })
            dem_data = src.read(1)
            dem_data = np.where(dem_data < 0, 0, dem_data)
            bounds = [src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top]
        return dem_data, bounds
    except RasterioIOError as e:
        st.error(f"Error opening the file: {str(e)}")
        return None, None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None, None

st.title("DEM Viewer")

uploaded_file = st.file_uploader("Choose a DEM TIFF file", type="tif")

if uploaded_file is not None:
    st.write(f"File size: {uploaded_file.size} bytes")
    dem_data, bounds = process_dem(uploaded_file)
    
    if dem_data is not None and bounds is not None:
        m = folium.Map(location=[(bounds[1]+bounds[3])/2, (bounds[0]+bounds[2])/2], zoom_start=10)
        
        colormap = LinearColormap(colors=['blue', 'green', 'yellow', 'orange', 'red'], 
                                  vmin=dem_data.min(), vmax=dem_data.max())
        
        raster_layers.ImageOverlay(
            dem_data,
            bounds=bounds,
            colormap=colormap,
            opacity=0.7
        ).add_to(m)
        
        colormap.add_to(m)
        
        folium.LatLngPopup().add_to(m)

        map_data = folium_static(m, width=700, height=500)

        st.write(f"DEM statistics:")
        st.write(f"Min elevation: {dem_data.min():.2f} meters")
        st.write(f"Max elevation: {dem_data.max():.2f} meters")
        st.write(f"Mean elevation: {dem_data.mean():.2f} meters")

        # Get clicked location
        loc = get_geolocation()
        
        if loc:
            st.write(f"Clicked coordinates: Latitude {loc['coords']['latitude']:.6f}, Longitude {loc['coords']['longitude']:.6f}")
        else:
            st.write("Click on the map to see coordinates")

    else:
        st.write("Unable to process the uploaded file. Please ensure it's a valid DEM TIFF file.")
else:
    st.write("Please upload a DEM TIFF file to view it on the map.")
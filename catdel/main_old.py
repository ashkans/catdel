import io
from pathlib import Path
import matplotlib.pyplot as plt
import streamlit as st

from catdel import process
from catdel.visualization import pyplot as pp
from catdel.components import misc 




def main():
    config = {'snap_thr':1000}
    # Create output directory
    op = Path('./catchment_output')
    op.mkdir(exist_ok=True, parents=True)

    # Read elevation raster
    st.write("## Digital Elevation Map")
    uploaded_file = st.file_uploader("Upload a DEM file", type=["tif"])

    if uploaded_file is not None:
        # Read the file from the uploaded file buffer
        file_buffer = io.BytesIO(uploaded_file.getvalue())
        grid, dem = process.load_grid_and_data(file_buffer)

        misc.options(grid, config)

        if st.button('Delineate'):
 
            o = process.delin(dem, grid, config)
            

            fig, ax=plt.subplots(figsize=(15,15))
            pp.add_raster(dem, grid, ax)
            pp.add_raster(o['catch'], grid, ax)
            pp.add_outlets(config, ax)
            pp.add_river_system(o['branches'], ax)
            st.pyplot(fig)
            plt.close(fig)

        else:
            fig, ax=plt.subplots(figsize=(15,15))
            pp.add_raster(dem, grid, ax)
            pp.add_outlets(config, ax)
            st.pyplot(fig)
            plt.close(fig)


# Run the main function
if __name__ == '__main__':
    main()

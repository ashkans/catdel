from catdel.state_manager import StateManager
from catdel.process import input_output
from io import BytesIO

sm = StateManager.get_instance()

def load_dem_and_grid():
    
    # process file to get dem and grid
    if sm.dem_file:
        
        file_buffer = BytesIO(sm.dem_file.getvalue())
        dem, grid = input_output.load_grid_and_data(file_buffer, sm.config.proj.pyproj)
        sm.dem=dem
        sm.grid=grid    
    
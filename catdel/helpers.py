from catdel.state_manager import StateManager
from catdel.process import input_output
from io import BytesIO

from catdel.process import dem_processing as dp

sm = StateManager.get_instance()

def load_dem_and_grid():
    
    # process file to get dem and grid
    if sm.dem_file and sm.dem is None:
        
        file_buffer = BytesIO(sm.dem_file.getvalue())
        dem, grid = input_output.load_grid_and_data(file_buffer, sm.config.proj.pyproj)
        sm.dem=dem
        sm.grid=grid  

        
        sm.all_branches = dp.all_streams(sm.dem, sm.grid, sm.config.acc_thr, sm.config.dst_crs)
    
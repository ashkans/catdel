import streamlit as st
from catdel.state_manager import StateManager
from catdel.add_ga import inject_ga_if_on_server
from catdel.components.dem_uploader import DemUploader
from catdel.components.map import Map
from catdel.helpers import load_dem_and_grid


sm = StateManager.get_instance()


# initialize
inject_ga_if_on_server()



def main():


    du = DemUploader()
    du()

    load_dem_and_grid()

    m = Map()
    m()
    
    # map

    


if __name__ == '__main__':
    main()


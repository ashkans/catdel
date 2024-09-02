from catdel.components.base_component import BaseComponent
import streamlit as st
from catdel.state_manager import StateManager
sm = StateManager.get_instance()


class DemUploader(BaseComponent):
    def call(self):
        with st.expander('', expanded=sm.dem is None, icon=':material/upload:'):
            self.core()

    def core(self):
        dem_file = st.file_uploader("uploader",
        type=["tif"],
        key='file_upload',
        on_change=self.file_uploader_on_change,
        accept_multiple_files=False,
        label_visibility='collapsed',
        )

        sm.dem_file = dem_file

    @staticmethod
    def file_uploader_on_change():
        StateManager.get_instance(reset=True)
    
    def save_file(self):
        raise NotImplementedError


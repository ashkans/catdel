import streamlit as st
from catdel.config import Config
from datetime import datetime


 
class StateManager:
    def __init__(self):
        self._boolean_states = {
            'showStreams':True,
            'streamsAdded':False,
            'catchmentAdded':False,
            'showCatchment':True,
            'boundaryAdded':False,
            'needsRender': True,
            'outletMarkerUpdate': False,
            'showOutlet': True,
            'outletAdded': False,
            'lastClickHolderAdded':False,
            'allStreamsAdded': False,
            'allStreamsCalculated': False,
        }
        self._other_states = ['map', 'delin', 'grid', 'dem', 'outlet_lat', 'outlet_lng', 'allStreams', 'uploaded_file', 'map_outputs']
        self._initialize_booleans()
        self._initialize_config()
        self._initialize_other()
        self._create_properties()
        st.session_state['state_manager'] = self

        self.session_start_time = datetime.now()

    def _initialize_booleans(self):
        for key, value in self._boolean_states.items():
            st.session_state[key] = value

    def _initialize_config(self):
        if 'config' not in st.session_state:
            st.session_state['config'] = Config()

    def _initialize_other(self):

        for key in self._other_states:
            st.session_state[key] = None

    @property
    def seession_id(self):
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        return ctx.session_id   


    def _create_properties(self):
        for state in list(self._boolean_states.keys()) + self._other_states + ['config']:
            setattr(StateManager, state, self._create_property(state))

    @property
    def outlet(self):
        if self.map_outputs is not None:
            if self.map_outputs['last_clicked'] is not None:
                return self.map_outputs['last_clicked']['lat'],self.map_outputs['last_clicked']['lng']
        


    def _create_property(self, state):
        def getter(self):
            return st.session_state.get(state, False)
        
        def setter(self, value):
            st.session_state[state] = value
        
        return property(getter, setter)

    @staticmethod
    def get_states(*args):
        return [st.session_state[key] for key in args]

    @staticmethod
    def get_state(key):
        return st.session_state[key]


    @staticmethod
    def add_states(**kwargs):
        st.session_state.update(kwargs)

    
    @staticmethod
    def get_instance(reset=False):
        if 'state_manager' not in st.session_state or reset:
            StateManager()
        return st.session_state.state_manager
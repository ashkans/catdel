import streamlit as st
from catdel.config import Config


class StateManager:
    def __init__(self):
        """Initializes the StateManager and sets up the initial states."""
        self._boolean_states: dict[str, bool] = {'all_rivers_plotted': False, 'catchment_plotted': False}
        self._other_states: list[str] = ['dem_file', 'dem', 'map', 'grid', 'map_outputs', 'all_branches', 'delin_results', 'catchment_boundaries_fg']
        
        self._initialize_booleans()
        self._initialize_other()
        self._initialize_config()
        self._create_properties()
        
        self._outlet = None
        st.session_state['state_manager'] = self

    def _initialize_booleans(self) -> None:
        """Initializes boolean states in Streamlit session state."""
        for key, value in self._boolean_states.items():
            st.session_state[key] = value

    def _initialize_config(self) -> None:
        """Initializes configuration in Streamlit session state."""
        if 'config' not in st.session_state:
            st.session_state['config'] = Config()

    def _initialize_other(self) -> None:
        """Initializes other states in Streamlit session state."""
        for key in self._other_states:
            st.session_state[key] = None

    def _create_properties(self) -> None:
        """Creates properties for boolean and other states."""
        for state in list(self._boolean_states.keys()) + self._other_states + ['config']:
            setattr(StateManager, state, self._create_property(state))

    def _create_property(self, state: str) -> property:
        """
        Creates a property for a given state.
        
        Args:
            state (str): The name of the state to create a property for.
        
        Returns:
            property: A property object with getter and setter methods.
        """
        def getter(self) -> any:
            """Gets the value of the state."""
            return st.session_state.get(state, False)

        def setter(self, value: any) -> None:
            """Sets the value of the state."""
            st.session_state[state] = value

        return property(getter, setter)

    @staticmethod
    def get_states(*args: str) -> list[any]:
        """
        Gets the values of multiple states from Streamlit session state.
        
        Args:
            *args (str): The names of the states to retrieve.
        
        Returns:
            list[any]: A list of the values of the specified states.
        """
        return [st.session_state[key] for key in args]

    @staticmethod
    def get_state(key: str) -> any:
        """
        Gets the value of a single state from Streamlit session state.
        
        Args:
            key (str): The name of the state to retrieve.
        
        Returns:
            any: The value of the specified state.
        """
        return st.session_state[key]

    @staticmethod
    def add_states(**kwargs: any) -> None:
        """
        Adds or updates states in Streamlit session state.
        
        Args:
            **kwargs (any): Key-value pairs of states to add or update.
        
        Returns:
            None
        """
        st.session_state.update(kwargs)

    @staticmethod
    def get_instance(reset: bool = False) -> 'StateManager':
        """
        Gets the instance of StateManager, creates it if not exists or reset is True.
        
        Args:
            reset (bool): If True, resets the StateManager instance. Defaults to False.
        
        Returns:
            StateManager: The instance of StateManager.
        """
        if 'state_manager' not in st.session_state or reset:
            StateManager()
        return st.session_state.state_manager

    @property
    def session_id(self) -> str:
        """
        Gets the session ID from Streamlit's script runner context.
        
        Returns:
            str: The session ID.
        """
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        return ctx.session_id


    @property
    def outlet(self) -> tuple[float, float] | None:
        """
        Gets the latitude and longitude of the last clicked point on the map.
        
        Returns:
            tuple[float, float] | None: A tuple containing latitude and longitude if available, otherwise None.
        """
        if self.map_outputs is not None:
            if self.map_outputs['last_clicked'] is not None:
                self._outlet = self.map_outputs['last_clicked']['lat'], self.map_outputs['last_clicked']['lng']
        return self._outlet
    
    @property
    def outlet_geo(self) -> tuple[float, float]:
        if self.outlet is not None:
            lat, lng = self.outlet
            return self.config.proj.from_geo(lat, lng)        

    
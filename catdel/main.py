import streamlit as st
from catdel.state_manager import StateManager
from catdel.add_ga import inject_ga_if_on_server
sm = StateManager.get_instance()


# initialize
inject_ga_if_on_server()


def main():
    pass
import yaml
from catdel.projection import Projection
from typing import Any, Dict
import streamlit as st


default_config: Dict[str, Any] = {
    # Placeholder for default configuration settings
    "page_config": {
        "page_title": "Default Title",
        "page_icon": "🐱",
        "layout": "centered",
        "initial_sidebar_state": "auto"
    }
}


class Config:
    def __init__(self) -> None:
        """Initializes the configuration with default settings."""
        self._config = default_config.copy()  # Make a copy of default_config

    def __getattr__(self, name: str) -> Any:
        """Gets a configuration attribute.

        Args:
            name (str): The name of the configuration attribute.

        Returns:
            Any: The value of the configuration attribute.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        try:
            return self._config[name]
        except KeyError:
            raise AttributeError(f"'Config' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """Sets a configuration attribute.

        Args:
            name (str): The name of the configuration attribute.
            value (Any): The value to set.
        """
        if name == '_config':
            super().__setattr__(name, value)
        else:
            self._config[name] = value

    def __getitem__(self, name: str) -> Any:
        """Gets a configuration item using dictionary-like access.

        Args:
            name (str): The name of the configuration item.

        Returns:
            Any: The value of the configuration item.

        Raises:
            AttributeError: If the item does not exist.
        """
        try:
            return self._config[name]
        except KeyError:
            raise AttributeError(f"'Config' object has no attribute '{name}'")

    def save(self, file_path: str) -> None:
        """Saves the configuration to a YAML file.

        Args:
            file_path (str): The path to the file where the configuration will be saved.
        """
        with open(file_path, 'w') as f:
            yaml.dump(self._config, f)

    @property
    def proj(self) -> Projection:
        """Gets the Projection object associated with this configuration.

        Returns:
            Projection: The Projection object.
        """
        return Projection(self)

    @staticmethod
    def load(file_path: str) -> 'Config':
        """Loads a configuration from a YAML file.

        Args:
            file_path (str): The path to the YAML file.

        Returns:
            Config: The loaded Config object.
        """
        with open(file_path, 'r') as f:
            config_data = yaml.safe_load(f)
        config = Config()
        config._config.update(config_data)
        return config

    def set_page_config(self) -> None:
        """Sets the Streamlit page configuration using the settings from the configuration."""
        try:
            page_config = self._config["page_config"]
            st.set_page_config(**page_config)
        except KeyError:
            raise AttributeError("'Config' object has no 'page_config' attribute")


# Example usage:
if __name__ == "__main__":
    config = Config.load("config.yaml")
    config.set_page_config()

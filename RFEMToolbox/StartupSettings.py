import os
import json


class StartupSettings:
    """Facade for accessing settings."""

    @staticmethod
    def load_settings():
        """Creates an instance of SettingsRepository."""
        return SettingsRepository()


class SettingsRepository:
    """Handles loading and accessing application settings."""

    def __init__(self):
        """Initialize and load settings."""
        self._file_path = os.path.join("RFEMToolbox", "start-settings.json")
        self._settings_dict = self._load_settings()

    def _load_settings(self):
        """Loads settings from the JSON file."""
        try:
            with open(self._file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {self._file_path} was not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from the file {self._file_path}.")
            return {}

    def _get_setting(self, key, default=None):
        """Retrieve a specific setting value."""
        return self._settings_dict.get("startup", {}).get(key, default)

    @property
    def model_path(self):
        """Returns the model path."""
        return self._get_setting("modelPath", "")

    @property
    def model_name(self):
        """Returns the model name."""
        return self._get_setting("modelName", "")

    @property
    def save_path(self):
        """Returns the save path."""
        return self._get_setting("savePath", "")

    @property
    def displacement_direction(self):
        """Returns the displacement direction."""
        return self._get_setting("displacementDirection", "")

    @property
    def fe_mesh_size(self):
        """Returns the initial finite element mesh size."""
        return self._get_setting("initialFeMeshSize", 0.0)

    @property
    def steps(self):
        """Returns the incremental steps."""
        return self._get_setting("incrementalSteps", 0.0)

    @property
    def json_save_path(self):
        """Returns the JSON save path."""
        return self._get_setting("jsonSavePath", "")
    
    @property
    def node_number(self):
        """Returns the node number"""
        return self._get_setting("nodeNumber", "")


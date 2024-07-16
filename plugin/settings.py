import os
import json

class Settings:

    plugins_dir = os.path.dirname(os.getcwd())
    plugins_parent_dir = os.path.dirname(plugins_dir)
    settings_file_path = os.path.join(plugins_parent_dir, "Settings", "Settings.json")

    default_language = "en"

    def __init__(self):
        pass

    @staticmethod
    def get_language():

        if os.path.exists(Settings.settings_file_path):
            with open(Settings.settings_file_path) as f:
                data = json.load(f)
                return data.get('Language', Settings.default_language)
        else:
            return Settings.default_language

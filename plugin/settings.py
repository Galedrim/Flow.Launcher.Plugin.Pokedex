import os
import pathlib
import json

class Settings:

    roamingDataPath = pathlib.Path(os.path.join(os.getenv("APPDATA"), "FlowLauncher/Settings/"))
    settingsFilePath = os.path.join(roamingDataPath, "Settings.json")

    def __init__(self):
        pass

    @staticmethod
    def get_language():
        with open(Settings.settingsFilePath) as f:
            data = json.load(f)
        return data['Language']

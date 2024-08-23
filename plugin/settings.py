import os
import json

class Settings:

    DEFAULT_LANGUAGE  = "en"
    VALID_LANGUAGES = {'en', 'fr'}

    def __init__(self):
        pass

    def get_language():
        
        plugins_parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))
        settings_file_path = os.path.join(plugins_parent_dir, "Settings", "Settings.json")

        if os.path.exists(settings_file_path):
            try:
                with open(settings_file_path, 'r') as f:
                    data = json.load(f)
                    language = data.get('Language', Settings.DEFAULT_LANGUAGE)
                    if language in Settings.VALID_LANGUAGES:
                        return language
                    else:
                        return Settings.DEFAULT_LANGUAGE
            except (json.JSONDecodeError, IOError):
                return Settings.DEFAULT_LANGUAGE
        else:
            return Settings.DEFAULT_LANGUAGE
import json

TYPE_JSON_FILE = r".\data\types.json"

class Type:
    def __init__(self, data):
        self.name = {
            'fr': data['name_fr'],
            'en': data['name_en']
        }
        self.emoji = data['emoji']

class TypeLoader:
    def __init__(self):
        with open(TYPE_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.types_dict = {item['name_fr']: Type(item) for item in data}

    def get_type_by_french_name(self, name):
        return self.types_dict.get(name)
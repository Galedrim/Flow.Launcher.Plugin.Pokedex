import json

ABILITY_FR_JSON_FILE = r".\data\abilities\abilities_fr-FR.json"
ABILITY_EN_JSON_FILE = r".\data\abilities\abilities_en-US.json"

class Ability:
    def __init__(self, data):
        self.name = {
            'fr': data['name_fr'],
            'en': data['name_en']
        }
        self.description = {
            'fr': data['description'],
            'en': None
        }

    def get_name(self, language) :
        if self.name:
            if language == 'fr':
                return f"{self.name['fr']} | {self.name['en']}"
            else:
                return f"{self.name['en']}"
        return ""
    
    def get_description(self, language):
        if self.description:
            if language == 'fr':
                return f"{self.description['fr']}"
            else:
                return f"{self.description['en']}"
        return ""

class AbilityLoader:
    def __init__(self):
        with open(ABILITY_FR_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            ability_dict_en_incomplete  = {item['name_en']: Ability(item) for item in data}
            self.ability_dict_fr = {item['name_fr']: Ability(item) for item in data}

        with open(ABILITY_EN_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.ability_dict_en = self.set_english_descriptions(data, ability_dict_en_incomplete)

    @staticmethod
    def set_english_descriptions(data, ability_dict):
        for item in data:
            if ability_dict.get(item['name']):
                ability_dict.get(item['name']).description['en'] = item['description']
        return ability_dict

    def get_ability_by_french_name(self, name_fr):
        return self.ability_dict_fr.get(name_fr)
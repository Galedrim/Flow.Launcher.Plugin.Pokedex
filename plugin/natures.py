import json

NATURE_JSON_FILE = r".\data\natures.json"

class Nature:

    def __init__(self, data):
        self.name = {
            'en': data['name_en'],
            'fr': data['name_fr']
        }
        self.atk_phy = data['atk']
        self.def_phy = data['def']
        self.spe_atk = data['spe_atk']
        self.spe_def = data['spe_def']
        self.spd = data['spd']

    def get_name(self, language):
        if self.name:
            if language == 'fr':
                return f"{self.name['fr']} | {self.name['en']}"
            else:
                return f"{self.name['en']}"
        return ""

    def get_stats(self):
        stats_list = []

        if self.atk_phy:
            stats_list.append(f"Atk {self.atk_phy}")
        if self.def_phy:
            stats_list.append(f"Def {self.def_phy}")
        if self.spe_atk:
            stats_list.append(f"SpAtk {self.spe_atk}")
        if self.spe_def:
            stats_list.append(f"SpDef {self.spe_def}")
        if self.spd:
            stats_list.append(f"Spd {self.spd}")

        if stats_list:
            return f"{' | '.join(stats_list)}"
        return "/"

class NatureLoader:
    def __init__(self):
        with open(NATURE_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.nature_dict = {item['name_fr']: Nature(item) for item in data}

    def get_nature(self, name_fr):
        return self.nature_dict.get(name_fr)
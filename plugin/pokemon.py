from sprites import Sprites

class Ability:
    def __init__(self, data):
        self.name = {
            'fr': data['name_fr'],
            'en': data['name_en']
        }
        self.description = data['description']

    def display_name(self, language):
        if self.name:
            if language == "fr":
                return f"{self.name['fr']} | {self.name['en']}"
            else:
                return f"{self.name['en']}"
        return ""
    
    def display_description(self):
        if self.description:
            return f"{self.description}"
        return ""

class Nature:
    def __init__(self, data):
        self.name = {
            'fr': data['name_fr'],
            'en': data['name_en']
        }
        self.atk_phy = data['atk']
        self.def_phy = data['def']
        self.spe_atk = data['spe_atk']
        self.spe_def = data['spe_def']
        self.spd = data['spd']

    def display_name(self, language):
        if self.name:
            if language == "fr":
                return f"{self.name['fr']} | {self.name['en']}"
            else:
                return f"{self.name['en']}"
        return ""
    
    def display_stats(self):
        nature_list = []
        
        if self.atk_phy:
            nature_list.append(f"Atk {self.atk_phy}")
        if self.def_phy:
            nature_list.append(f"Def {self.def_phy}")
        if self.spe_atk:
            nature_list.append(f"SpAtk {self.spe_atk}")
        if self.spe_def:
            nature_list.append(f"SpDef {self.spe_def}")
        if self.spd:
            nature_list.append(f"Spd {self.spd}")

        if nature_list:
            return f"{' | '.join(nature_list)}"
        return "/"

class Type:
    def __init__(self, data):
        self.name = {
            'fr': data['name_fr'],
            'en': data['name_en']
        }
        self.emoji = data['emoji']

class Pokemon:
    def __init__(self, data):
        self.pokedex_id = data['pokedex_id']
        self.generation = data['generation']
        self.name = {
            'fr': data['name']['fr'],
            'en': data['name']['en']
        }
        self.types = data['types']
        self.abilities = data['abilities']
        self.evolutions = data['evolutions']
        self.stats = data['stats']
        self.formes = data['formes']
        self.icon = Sprites.get_icon(self.pokedex_id)

    def display_name(self, language):
        if self.pokedex_id and self.name:
            if language == "fr":
                return f"#{self.pokedex_id:04} - {self.name['fr']} | {self.name['en']}"
            else:
                return f"#{self.pokedex_id:04} - {self.name['en']}"
        return ""

    def display_types(self, types_list, language):
        if self.types:
            type_emoji_list = []
            for pokemon_type in self.types:
                for type_item in types_list:
                    if type_item.name['fr'].lower() == pokemon_type['name'].lower():
                        type_emoji = f"{type_item.emoji} {type_item.name[language]} "
                        type_emoji_list.append(type_emoji)
            return f"{' | '.join(type_emoji_list)}"
        return ""

    def display_evolutions(self):
        if self.evolutions:
            evolutions_list = []
            if self.evolutions['pre']:
                for pre_evolution in self.evolutions['pre'] :
                    evolutions_list.append(f"{pre_evolution['name']} <")

            evolutions_list.append("X")

            if self.evolutions['next']:
                for next_evolution in self.evolutions['next']:
                    evolutions_list.append(f"> {next_evolution['name']}")
            return f"{' '.join(evolutions_list)}"
        return ""

    def display_abilities(self):
        if self.abilities:
            name_ability = [ability['name'] for ability in self.abilities]
            return f"{' | '.join(name_ability)}"
        return ""

    def display_stats(self):
        if self.stats:
            return (
                f"{self.stats['hp']} HP | "
                f"{self.stats['atk']} Atk | "
                f"{self.stats['def']} Def | "
                f"{self.stats['spe_atk']} SpAtk | "
                f"{self.stats['spe_def']} SpDef | "
                f"{self.stats['spd']} Spd"
            )
        return ""

import json

from plugin.sprites import Sprite
from plugin.abilities import AbilityLoader
from plugin.types import TypeLoader

POKEMON_JSON_FILE = r".\data\pokemons\pokemons.json"
POKEMON_REGIONAL_JSON_FILE = r".\data\pokemons\pokemons_regional.json"
POKEMON_MEGA_JSON_FILE = r".\data\pokemons\pokemons_mega.json"

class Region:
    def __init__(self, name, pokemons):
        self.name = name
        self.pokemons = pokemons

class Pokemon:
    def __init__(self, pokedex_id, generation, name_en, name_fr):
        self.pokedex_id = pokedex_id
        self.generation = generation
        self.name = {
            'en': name_en,
            'fr': name_fr
        }
        self.types = {
            'fr': [], 
            'en': [],
            'emoji': [] 
        }
        self.abilities = {
            'fr': [], 
            'en': []
        }
        self.stats = {}
        self.pre_evolutions = {
            'fr': [], 
            'en': []
        }
        self.next_evolutions = {
            'fr': [], 
            'en': []
        }
        self.base_forms = {
            'fr': None, 
            'en': None
        }
        self.regional_forms = {
            'fr': [], 
            'en': [],
            'region': [] 
        }
        self.sprite = None

    def get_name(self, language):
        if self.pokedex_id and self.name:
            if language == 'fr':
                return f"#{self.pokedex_id:04} - {self.name['fr']} | {self.name['en']}"
            else:
                return f"#{self.pokedex_id:04} - {self.name['en']}"
        return ""

    def get_types(self, language):
        if self.types:
            return ' | '.join(
                f"{self.types['emoji'][index]} {item}"
                for index, item in enumerate(self.types[language])
            )
        return ""

    def get_abilities(self, language):
        if self.abilities[language]:
            return ' | '.join(
                f"{item}"
                for item in self.abilities[language]
            )
        return ""
    
    def get_stats(self, language):
        if self.stats:
            if language == 'fr':
                return (
                    f"{self.stats['hp']} PV | "
                    f"{self.stats['atk']} Atk | "
                    f"{self.stats['def']} Def | "
                    f"{self.stats['spe_atk']} SpAtk | "
                    f"{self.stats['spe_def']} SpDef | "
                    f"{self.stats['spd']} Vit"
                )
            else:
                return (
                    f"{self.stats['hp']} HP | "
                    f"{self.stats['atk']} Atk | "
                    f"{self.stats['def']} Def | "
                    f"{self.stats['spe_atk']} SpAtk | "
                    f"{self.stats['spe_def']} SpDef | "
                    f"{self.stats['spd']} Spd"
                )
        return ""

    def get_evolutions(self, language):
        evolutions_list = []
        if self.pre_evolutions[language]:
            for pre_evolution in self.pre_evolutions[language]:
                evolutions_list.append(f"{pre_evolution} >")

        evolutions_list.append("X")

        if self.next_evolutions[language]:
            for next_evolution in self.next_evolutions[language]:
                evolutions_list.append(f"> {next_evolution}")
        
        return f"{' '.join(evolutions_list)}"

    def get_icon(self):
        if self.sprite:
            return self.sprite
        return ""

class PokemonLoader:
    def __init__(self):

        self.ability_loader = AbilityLoader()
        self.type_loader = TypeLoader()

        self.pokemon_base_dict = self.set_pokemon_base_dict()
        self.pokemon_regional_dict = self.set_pokemon_regional_dict()
        self.pokemon_mega_dict = self.set_pokemon_mega_dict()

    def set_pokemon_base_dict(self):
        with open(POKEMON_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            pokemon_base_dict = {}
            for item in data:
                pokemon = Pokemon(item['pokedex_id'], item['generation'], item['name']['en'], item['name']['fr'])
                self.set_base_information(item, pokemon)
                self.set_french_evolutions_information(item, pokemon)
                self.set_regional_form(item, pokemon)
                self.set_sprite(pokemon)
                pokemon_base_dict[pokemon.name['fr']] = pokemon

            for name, pokemon in pokemon_base_dict.items():
                self.set_english_evolutions_information(pokemon_base_dict, pokemon)

        return pokemon_base_dict

    def set_pokemon_regional_dict(self):
        with open(POKEMON_REGIONAL_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            pokemon_regional_dict = {}
            pokemon_base_dict = self.pokemon_base_dict

            for form, pokemons in data.items():
                for item in pokemons.values():
                    pokemon_regional = Pokemon(item['pokedex_id'], item['generation'], item['name']['en'], item['name']['fr'])
                    self.set_base_information(item, pokemon_regional)
                    self.set_french_evolutions_information(item, pokemon_regional)
                    self.set_base_form(pokemon_base_dict, pokemon_regional)
                    self.set_sprite(pokemon_regional)
                    pokemon_regional_dict[pokemon_regional.name['fr']] = pokemon_regional

            for name, pokemon in pokemon_regional_dict.items():
                self.set_english_evolutions_information(pokemon_regional_dict, pokemon)

            return pokemon_regional_dict

    def set_pokemon_mega_dict(self):
        with open(POKEMON_MEGA_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            pokemon_mega_dict = {}
            for pokemons in data:
                for item in pokemons['formes']:
                    pokemon_mega = Pokemon(pokemons['pokedex_id'], pokemons['generation'], item['name']['en'], item['name']['fr'])
                    self.set_base_information(item, pokemon_mega)
                    pokemon_mega.pre_evolutions['fr'].append(pokemons['name']['fr'])
                    pokemon_mega.pre_evolutions['en'].append(pokemons['name']['en'])
                    self.set_sprite(pokemon_mega)
                    pokemon_mega_dict[pokemon_mega.name['fr']] = pokemon_mega

            return pokemon_mega_dict

    def set_base_information(self, item, pokemon):
        self.set_stats(item, pokemon)
        self.set_types(self.type_loader, item, pokemon)
        self.set_abilities(self.ability_loader, item, pokemon)

    def set_french_evolutions_information(self, item, pokemon):
        self.set_french_previous_evolution(item, pokemon)
        self.set_french_next_evolution(item, pokemon)

    def set_english_evolutions_information(self, pokemon_dict, pokemon):
        self.set_english_previous_evolution(pokemon_dict, pokemon)
        self.set_english_next_evolution(pokemon_dict, pokemon)

    @staticmethod
    def set_stats(item, pokemon):
        pokemon.stats = item['stats']

    @staticmethod
    def set_types(loader, item, pokemon):
        for pokemon_type in item['types']:
            type_loaded = loader.get_type_by_french_name(pokemon_type['name'])
            if type_loaded is not None:
                pokemon.types['fr'].append(type_loaded.name['fr'])
                pokemon.types['en'].append(type_loaded.name['en'])
                pokemon.types['emoji'].append(type_loaded.emoji)

    @staticmethod
    def set_abilities(loader, item, pokemon):
        for pokemon_ability in item['abilities']:
            ability_loaded = loader.get_ability_by_french_name(pokemon_ability['name'])
            if ability_loaded is not None:
                pokemon.abilities['fr'].append(ability_loaded.name['fr'])
                pokemon.abilities['en'].append(ability_loaded.name['en'])

    @staticmethod
    def set_french_previous_evolution(item, pokemon):
        if item['evolutions']:
            evolutions = item['evolutions']
            if evolutions['pre']:
                pokemon.pre_evolutions['fr'] = [pre_evolution['name'] for pre_evolution in evolutions['pre']]

    @staticmethod
    def set_french_next_evolution(item, pokemon):
        if item['evolutions']:
            evolutions = item['evolutions']
            if evolutions['next']:
                pokemon.next_evolutions['fr'] = [next_evolution['name'] for next_evolution in evolutions['next']]

    @staticmethod
    def set_english_previous_evolution(pokemon_dict, pokemon):
        for pre_evolution in pokemon.pre_evolutions['fr']:
            pre_evolution_loaded = pokemon_dict.get(pre_evolution)
            if pre_evolution_loaded is not None:
                pokemon.pre_evolutions['en'].append(pre_evolution_loaded.name['en'])

    @staticmethod
    def set_english_next_evolution(pokemon_dict, pokemon):
        for next_evolution in pokemon.next_evolutions['fr']:
            next_evolution_loaded = pokemon_dict.get(next_evolution)
            if next_evolution_loaded is not None:
                pokemon.next_evolutions['en'].append(next_evolution_loaded.name['en'])

    @staticmethod
    def set_regional_form(item, base_pokemon):
        if item['formes']:
            for form in item['formes']:
                base_pokemon.regional_forms['region'] = form['region']
                if form['name']:
                    base_pokemon.regional_forms['fr'] = form['name']['fr']
                    base_pokemon.regional_forms['en'] = form['name']['en'].lower()

    @staticmethod
    def set_base_form(pokemon_dict, regional_pokemon):
        for name, pokemon in pokemon_dict.items():
            if pokemon.regional_forms['en'] == regional_pokemon.name['en'].lower():
                regional_pokemon.base_forms['fr'] = pokemon.name['fr']
                regional_pokemon.base_forms['en'] = pokemon.name['en'].lower()

    @staticmethod
    def set_sprite(pokemon):
        pokemon.sprite = Sprite.get_icon(pokemon.pokedex_id)

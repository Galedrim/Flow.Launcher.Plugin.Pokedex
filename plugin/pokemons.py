import json

from sprites import Sprites
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
    def __init__(self):
        self.pokedex_id = None
        self.generation = None
        self.name = {
            'en': None,
            'fr': None
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
    
    def get_stats(self):
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
        return Sprites.get_icon(self.pokedex_id, None)

class PokemonLoader:
    def __init__(self):

        with open(POKEMON_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            pokemon_list = self.set_pokemon(data)

        self.set_english_evolution(pokemon_list)

        with open(POKEMON_REGIONAL_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            # for region, pokemons in data.items():
            #     for pokemon in pokemons.values():
            #         if pokemon is not None:
            #             pokemon_regional = Pokemon(pokemon)
            #             self.pokemons_regional_list.append(pokemon_regional)

        with open(POKEMON_MEGA_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            # for pokemon in data:
            #     pokedex_id = pokemon['pokedex_id']
            #     for item in pokemon['formes']:
            #         mega_evolution = Pokemon(item)
            #         mega_evolution.pokedex_id = pokedex_id
            #         self.pokemons_list.append(mega_evolution)

        self.pokemon_list = pokemon_list

    @staticmethod
    def set_pokemon(data):
        pokemon_list = []

        ability_loader = AbilityLoader()
        type_loader = TypeLoader()

        for item in data:
            pokemon = Pokemon()
            pokemon.pokedex_id = item['pokedex_id']
            pokemon.generation = item['generation']

            pokemon.name['fr'] = item['name']['fr']
            pokemon.name['en'] = item['name']['en']

            for pokemon_type in item['types']:
                type_loaded = type_loader.get_type_by_french_name(pokemon_type['name'])
                if type_loaded is not None:
                    pokemon.types['fr'].append(type_loaded.name['fr'])
                    pokemon.types['en'].append(type_loaded.name['en'])
                    pokemon.types['emoji'].append(type_loaded.emoji)

            for pokemon_ability in item['abilities']:
                ability_loaded = ability_loader.get_ability_by_french_name(pokemon_ability['name'])
                if ability_loaded is not None:
                    pokemon.abilities['fr'].append(ability_loaded.name['fr'])
                    pokemon.abilities['en'].append(ability_loaded.name['en'])

            pokemon.stats = item['stats']

            if item['evolutions']:
                evolutions = item['evolutions']
                if evolutions['pre']:
                    pokemon.pre_evolutions['fr'] = [pre_evolution['name'] for pre_evolution in evolutions['pre']]
                if evolutions['next']:
                    pokemon.next_evolutions['fr'] = [next_evolution['name'] for next_evolution in evolutions['next']]

            pokemon_list.append(pokemon)

        return pokemon_list

    @staticmethod
    def set_english_evolution(pokemon_list):

        pokemon_names_dict = {}
        for pokemon in pokemon_list:
            pokemon_names_dict[pokemon.name['fr']] = pokemon.name['en']
        
        for pokemon in pokemon_list:
            for pre_evolution in pokemon.pre_evolutions['fr']:
                pre_evolution_loaded = pokemon_names_dict.get(pre_evolution)
                if pre_evolution_loaded is not None:
                    pokemon.pre_evolutions['en'].append(pre_evolution_loaded)

            for next_evolution in pokemon.next_evolutions['fr']:
                next_evolution_loaded = pokemon_names_dict.get(next_evolution)
                if next_evolution_loaded is not None:
                    pokemon.next_evolutions['en'].append(next_evolution_loaded)


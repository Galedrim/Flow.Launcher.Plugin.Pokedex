import json
import cattr

from dataclasses import dataclass, field
from typing import Dict

from pokemons.pokemons import Pokemon

POKEMONS_REGIONAL_JSON_FILE = r".\data\pokemons\regionals.json"
STARTING_REGIONS_ID = {'galar': 10161, 'alola': 10193, 'hisui': 10229, 'paldea': 10419}


@dataclass
class PokemonRegional:
    pokemon: Dict[str, Pokemon] = field(default_factory=dict)

@dataclass
class Region:
    name: Dict[str, PokemonRegional] = field(default_factory=dict)

class PokemonRegionalLoader:
    def __init__(self):
        with open(POKEMONS_REGIONAL_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            converter = cattr.Converter()

            regionals = {}
            region_ids = STARTING_REGIONS_ID.copy()
            for region, item in data.items():
                if region in region_ids:
                    for pokedex_id, pokemon in item.items():
                        region_key = region_ids.get(region)
                        regionals[region_key] = converter.structure(pokemon, Pokemon)
                        region_ids[region] += 1
                    self.pokemons = regionals
                else:
                    raise ValueError(f"No region found with name '{region}'")

    def _get_pokemons(self) -> Dict[str, Pokemon]:
        return self.pokemons
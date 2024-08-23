import json
import cattr

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from pokemons.pokemons import Pokemon

POKEMONS_NATIONALS_JSON_FILE = r".\data\pokemons\nationals.json"

@dataclass
class PokemonNational:
    pokemons: Dict[str, Pokemon] = field(default_factory=dict)

class PokemonNationalLoader:
    def __init__(self):
        with open(POKEMONS_NATIONALS_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            converter = cattr.Converter()
            pokemons = [converter.structure(item, Pokemon) for item in data]
            self.nationals = {str(pokemon.pokedex_id): pokemon for pokemon in pokemons}

    def _get_pokemons(self) -> Dict[str, Pokemon]:
        return self.nationals
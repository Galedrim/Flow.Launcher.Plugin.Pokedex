import json
import cattr

from dataclasses import dataclass, field
from typing import Dict, List, Optional

POKEMONS_MEGA_JSON_FILE = r".\data\pokemons\megas.json"
STARTING_ID = 10033

@dataclass
class MegaEvolution:
    name: Dict[str, str] = field(default_factory=lambda: {'fr': '', 'en': ''})
    types: List[Dict[str, str]] = field(default_factory=lambda: [{'name': ''}]) 
    abilities: List[Dict[str, str]] = field(default_factory=lambda: [{'name': ''}]) 
    stats: Dict[str, int] = field(default_factory=lambda: {
        'hp': 0, 'atk': 0, 'def': 0, 'spe_atk': 0, 'spe_def': 0, 'spd': 0
    })

@dataclass
class PokemonToMega:
    pokedex_id: int
    generation: int
    name: Dict[str, str] = field(default_factory=lambda: {'fr': '', 'en': ''})
    formes: List[MegaEvolution] = field(default_factory=list) 

class PokemonMegaLoader:
    def __init__(self):
        with open(POKEMONS_MEGA_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            converter = cattr.Converter()

            megas = {}
            megas_id = STARTING_ID
            for item in data:
                megas[str(megas_id)] = converter.structure(item, PokemonToMega)
                megas_id += 1
            
            self.megas = megas
        
    def _get_pokemons(self) -> Dict[str, MegaEvolution]:
        return self.megas
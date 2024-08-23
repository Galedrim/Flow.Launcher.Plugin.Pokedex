from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Evolutions:
    pre: Optional[List[Dict[str, str]]] = field(default_factory=lambda: {'pokedex_id': '', 'name': '','condition': ''})
    next: Optional[List[Dict[str, str]]] = field(default_factory=lambda: {'pokedex_id': '', 'name': '','condition': ''})

@dataclass
class Pokemon:
    pokedex_id: int
    generation: int
    name: Dict[str, str] = field(default_factory=lambda: {'fr': '', 'en': ''})
    types: List[Dict[str, str]] = field(default_factory=lambda: [{'name': ''}]) 
    abilities: List[Dict[str, str]] = field(default_factory=lambda: [{'name': ''}]) 
    stats: Dict[str, int] = field(default_factory=lambda: {
        'hp': 0, 'atk': 0, 'def': 0, 'spe_atk': 0, 'spe_def': 0, 'spd': 0
    })
    evolutions: Optional[Evolutions] = field(default_factory=Evolutions)
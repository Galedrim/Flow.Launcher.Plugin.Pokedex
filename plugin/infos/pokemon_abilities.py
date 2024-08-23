import json
import cattr

from dataclasses import dataclass, field
from typing import List, Dict

ABILITIES_JSON_FILE = r".\data\infos\pokemon_abilities.json"

@dataclass
class Ability:
    name: Dict[str, str] = field(default_factory=lambda: {'fr': '', 'en': ''})
    description: Dict[str, str] = field(default_factory=lambda: {'fr': '', 'en': ''})

class AbilityLoader:
    def __init__(self):
        with open(ABILITIES_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            converter = cattr.Converter()
            self.abilities = [converter.structure(item, Ability) for item in data]

    def _get_abilities(self) -> List[Ability]:
        return self.abilities
    
    def _get_ability(self, name: str) -> Ability:
        for a in self.abilities:
            if a.name.get('en').lower() == name.lower() or a.name.get('fr').lower() == name.lower():
                return a
        raise ValueError(f"No ability found with name '{name}'")
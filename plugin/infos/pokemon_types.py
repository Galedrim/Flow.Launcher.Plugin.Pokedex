import json
import cattr

from dataclasses import dataclass, field
from typing import List, Dict

TYPES_JSON_FILE = r".\data\infos\pokemon_types.json"

@dataclass
class Type:
    name: Dict[str, str] = field(default_factory=lambda: {'fr': '', 'en': ''})
    emoji: str = field(default_factory= "")

class TypeLoader:
    def __init__(self):
        with open(TYPES_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            converter = cattr.Converter()
            self.types = [converter.structure(item, Type) for item in data]

    def _get_types(self) -> List[Type]:
        return self.types
    
    def _get_type(self, name: str) -> Type:
        for t in self.types:
            if t.name.get('en').lower() == name.lower() or t.name.get('fr').lower() == name.lower():
                return t
        raise ValueError(f"No type found with name '{name}'")
import json
import cattr

from dataclasses import dataclass, field
from typing import List, Dict

NATURES_JSON_FILE = r".\data\infos\pokemon_natures.json"

@dataclass
class Nature:
    name: Dict[str, str] = field(default_factory=lambda: {'fr': '', 'en': ''})
    stats: Dict[str, str] = field(default_factory=lambda: {'atk': '', 'def': '', 'spe_atk': '','spe_def': '','spd': ''})

class NatureLoader:
    def __init__(self):
        with open(NATURES_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            converter = cattr.Converter()
            self.natures = [converter.structure(item, Nature) for item in data]

    def _get_natures(self) -> List[Nature]:
        return self.natures

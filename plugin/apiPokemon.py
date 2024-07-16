import json
from urllib import request
from settings import Settings

types_dict = {
    "Normal": ["Normal","🔶"],
    "Feu": ["Fire","🔥"],
    "Eau": ["Water", "💧"],
    "Plante":["Grass","🌳"],
    "Électrik": ["Electric","⚡"],
    "Glace": ["Ice","❄️"],
    "Combat": ["Fighting", "🥊"],
    "Poison": ["Poison","☠️"],
    "Sol": ["Ground","🏜️"],
    "Vol": ["Flying","🦅"],
    "Psy": ["Psychic","🧠"],
    "Insecte": ["Bug","🐛"],
    "Roche": ["Rock","🗿"],
    "Spectre": ["Ghost","👻"],
    "Dragon": ["Dragon","🐉"],
    "Ténèbres": ["Dark","🌑"],
    "Acier": ["Steel","⚙️"],
    "Fée": ["Fairy","✨"],
}

class ApiPokemon():

    @staticmethod
    def get_database():
        with request.urlopen("https://tyradex.vercel.app/api/v1/pokemon") as response:
            status_code = response.getcode()
            if status_code == 200:
                data = response.read().decode('utf-8') 
                return json.loads(data)

    @staticmethod
    def get_names(pokemon):
        return pokemon.get('name')

    @staticmethod
    def get_types(pokemon):
        types = pokemon.get('types')
        language = Settings.get_language()
        if types:
            type_strings = []
            for t in types:
                type_name = t['name']
                display_name = type_name if language == "fr" else types_dict[type_name][0]
                type_strings.append(f"{types_dict[type_name][1]} {display_name}")
            return f"-- {' / '.join(type_strings)}"
        return ""

    @staticmethod
    def get_evolution(pokemon):
        evolution = pokemon.get('evolution')
        if evolution and evolution.get('next'):
            next_evolution = evolution['next']
            for level in next_evolution:
                return f"Évolue en : {level['name']}"
        return ""


    @staticmethod
    def get_abilities(pokemon):
        talents = pokemon.get('talents')
        if talents:
            talent_names = [talent['name'] for talent in talents]
            return f"-- {' / '.join(talent_names)} --"
        return ""


    @staticmethod
    def get_stats(pokemon):
        stats = pokemon.get('stats')
        if stats:
            return (
                f"{stats['hp']} HP / "
                f"{stats['atk']} Atk / "
                f"{stats['def']} Def / "
                f"{stats['spe_atk']} SpA / "
                f"{stats['spe_def']} SpD / "
                f"{stats['vit']} Spe"
            )
        return ""

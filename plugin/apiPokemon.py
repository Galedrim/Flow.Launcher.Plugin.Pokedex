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

        if types is not None:
            if len(types) == 1:
                first_type = types[0]['name']

                if(language == "fr"):
                    return f"-- {types_dict[first_type][1]} {first_type}"
                else:
                    return f"-- {types_dict[first_type][1]} {types_dict[first_type][0]}"

            elif len(types) == 2:
                first_type = types[0]['name']
                second_type = types[1]['name']

                if(language == "fr"):
                    return f"-- {types_dict[first_type][1]} {first_type} / {types_dict[second_type][1]} {second_type}"
                else:
                    return f"-- {types_dict[first_type][1]} {types_dict[first_type][0]} / {types_dict[second_type][1]} {types_dict[second_type][0]}"
        return ""

    @staticmethod
    def get_evolution(pokemon):
        evolution = pokemon.get('evolution')
        language = Settings.get_language()

        if evolution is None:
            return ""
        else:
            next_evolution = evolution["next"]
            if next_evolution is None:
                return ""
            else:
                for level in next_evolution:
                    return f"Évolue en : {level['name']}"

    @staticmethod
    def get_abilities(pokemon):
        talents = pokemon.get('talents')

        if talents is None:
            return ""
        else:
            if len(talents) == 1:
                first_talent = talents[0]['name']
                return f"-- {first_talent} --"
            elif len(talents) == 2:
                first_talent = talents[0]['name']
                second_talent = talents[1]['name']
                return f"-- {first_talent} / {second_talent} --"
            elif len(talents) == 3:
                first_talent = talents[0]['name']
                second_talent = talents[1]['name']
                third_talent = talents[2]['name']
                return f"-- {first_talent} / {second_talent} / {third_talent} --"

    @staticmethod
    def get_stats(pokemon):
        stats = pokemon.get('stats') 
        if stats is None:
            return ""
        else:
            return (
                f"{stats['hp']} HP / "
                f"{stats['atk']} Atk  / "
                f"{stats['def']} Def  / "
                f"{stats['spe_atk']} SpA / "
                f"{stats['spe_def']} SpD / "
                f"{stats['vit']} Spe "
            )
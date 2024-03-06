import json
import os
import re
import webbrowser

from urllib import request
from flox import Flox

SPRITES_FOLDER = ".\sprites"
COUP_CRITIQUE_ICON = ".\Images\coup_critique.png"

type_emojis = {
    "Normal": "🔶",
    "Feu": "🔥",
    "Eau": "💧",
    "Plante": "🌳",
    "Electrik": "⚡",
    "Glace": "❄️",
    "Combat": "🥊",
    "Poison": "☠️",
    "Sol": "🏜️",
    "Vol": "🦅",
    "Psy": "🧠",
    "Insecte": "🐛",
    "Roche": "🗿",
    "Spectre": "👻",
    "Dragon": "🐉",
    "Ténèbres": "🌑",
    "Acier": "⚙️",
    "Fée": "✨",
}

class Pokedex(Flox):

    def results(self, query):
        with request.urlopen("https://tyradex.vercel.app/api/v1/pokemon") as response:
            status_code = response.getcode()
            if status_code == 200:
                data = response.read().decode('utf-8') 
                pokedex_data = json.loads(data)

        for pokemon in pokedex_data:
            if self.match(query, pokemon):
                self.add_item(
                    title=self.get_pokemon_names(pokemon),
                    subtitle=f'{self.get_pokemon_types(pokemon)} - {self.get_pokemon_talents(pokemon)}\n{self.get_pokemon_stats(pokemon)}',
                    icon=self.get_pokemon_sprites(pokemon),
                    context=self.get_pokemon_names(pokemon),
                    method = self.open_url,
                    parameters=[f"https://www.coupcritique.fr/search/{pokemon['name']['fr']}"]
                ) 

        return self._results

    def match(self, query, pokemon):
        if query == '':
            return True
        q = query.lower()

        pokemon_name_en = pokemon['name']['en']
        if q in pokemon_name_en.lower():
            return True

        pokemon_name_fr = pokemon['name']['fr']
        if q in pokemon_name_fr.lower():
            return True

    def get_pokemon_names(self, pokemon):
        names = pokemon.get('name')
        if names is not None:
            return f"{names['fr']} / {names['en']}"
        return "Nom: Inconnu"

    def get_pokemon_types(self, pokemon):
        types = pokemon.get('types')
        if types is not None:
            if len(types) == 1:
                first_type = types[0]['name']
                return f"Type: {self.get_icon_type(first_type)} {first_type}"
            elif len(types) == 2:
                first_type = types[0]['name']
                second_type = types[1]['name']
                return f"Types: {self.get_icon_type(first_type)} {first_type} / {self.get_icon_type(second_type)} {second_type}"
        return "Type: Inconnu"
    
    def get_icon_type(self, pokemon_type):
        return type_emojis.get(pokemon_type, '🔴')
    
    def get_pokemon_talents(self, pokemon):
        talents = pokemon.get('talents')
        if talents is not None:
            if len(talents) == 1:
                first_talent = talents[0]['name']
                return f"Talent: {first_talent}"
            elif len(talents) == 2:
                first_talent = talents[0]['name']
                second_talent = talents[1]['name']
                return f"Talents: {first_talent} / {second_talent}"
            elif len(talents) == 3:
                first_talent = talents[0]['name']
                second_talent = talents[1]['name']
                third_talent = talents[2]['name']
                return f"Talents: {first_talent} / {second_talent} / {third_talent}"
        return "Talent: Inconnu"

    def get_pokemon_stats(self, pokemon):
        stats = pokemon.get('stats') 
        if stats is not None:
            return (
                f"HP: {stats['hp']}, "
                f"ATK: {stats['atk']}, "
                f"DEF: {stats['def']}, "
                f"SATK: {stats['spe_atk']}, "
                f"SDEF: {stats['spe_def']}, "
                f"VIT: {stats['vit']}"
            )
        return "Stats: Inconnu"
    
    def get_pokemon_sprites(self, pokemon):
        found_file = None
        for files in os.listdir(SPRITES_FOLDER):
            pokemon_cleaned_name_en = self.clean_name(pokemon['name']['en'])
            if pokemon_cleaned_name_en in files:
                found_file = os.path.join(SPRITES_FOLDER, files)
                break
        return found_file
    
    def download_all_sprites(self, pokedex_data):
        for index, pokemon in enumerate(pokedex_data):
            sprite = self.get_pokemon_sprites(pokemon)
            with request.urlopen(sprite) as response:
                status_code = response.getcode()
                if status_code == 200:
                    pokemon_cleaned_name_en = self.clean_name(pokemon['name']['en'])
                    pokemon_cleaned_name_fr = self.clean_name(pokemon['name']['fr'])
                    filename = f"{index}_{pokemon_cleaned_name_en}_{pokemon_cleaned_name_fr}.png"
                    output_path = os.path.join(SPRITES_FOLDER, filename)
                    with open(output_path, "wb") as f:
                        f.write(response.read())
    
    def clean_name(self, name):
        cleaned_name = re.sub(r'[^\w\s-]', '', name)
        return cleaned_name
    
    def context_menu(self, data):
        self.add_item(
            title='Open Coupcritique.fr',
            subtitle='Open Coupcritique.fr',
            icon=COUP_CRITIQUE_ICON,
            method=self.open_url,
            parameters=[f'https://www.coupcritique.fr/']
        )

    def open_url(self, url):
        webbrowser.open(url)

    def query(self, query):
        self.results(query)
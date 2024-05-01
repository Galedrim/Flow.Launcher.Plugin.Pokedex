import os
import re
import json

from urllib import request

SPRITES_FOLDER = ".\sprites"

class Sprites:

    def __init__(self):
        pass

    @staticmethod
    def get_file(pokemon_name):
        found_file = None
        for files in os.listdir(SPRITES_FOLDER):
            if Sprites.clean(pokemon_name).lower() in files.lower():
                found_file = os.path.join(SPRITES_FOLDER, files)
                break
        return found_file
    
    @staticmethod
    def clean(pokemon_name):
        cleaned_name = re.sub(r'[^\w\s-]', '', pokemon_name)
        return cleaned_name

    @staticmethod
    def download_files():
        with request.urlopen("https://tyradex.vercel.app/api/v1/pokemon") as response:
            status_code = response.getcode()
            if status_code == 200:
                data = response.read().decode('utf-8') 
                pokedex_data = json.loads(data)

        for index, pokemon in enumerate(pokedex_data):
            sprite = Sprites.get_pokemon_sprites(pokemon)
            with request.urlopen(sprite) as response:
                status_code = response.getcode()
                if status_code == 200:
                    pokemon_cleaned_name_en = Sprites.clean_name(pokemon['name']['en'])
                    pokemon_cleaned_name_fr = Sprites.clean_name(pokemon['name']['fr'])
                    filename = f"{index}_{pokemon_cleaned_name_en}_{pokemon_cleaned_name_fr}.png"
                    output_path = os.path.join(SPRITES_FOLDER, filename)
                    with open(output_path, "wb") as f:
                        f.write(response.read())

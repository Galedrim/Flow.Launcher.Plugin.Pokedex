import os
SPRITES_DIR = r".\sprites"

class Sprite:

    index_map = {}

    @staticmethod
    def _get_basic_icon(pokedex_id: int):
        found_file = None
        formatted_id = f"{pokedex_id:04d}"

        for files in os.listdir(SPRITES_DIR):
            if formatted_id in files:
                found_file = os.path.join(SPRITES_DIR, files)
                break

        return found_file

    @staticmethod
    def _get_variant_icon(pokedex_id: int):
        found_file = None
        formatted_id = f"{pokedex_id:04d}"

        if pokedex_id in Sprite.index_map:
            Sprite.index_map[pokedex_id] += 1
        else:
            Sprite.index_map[pokedex_id] = 1

        index = Sprite.index_map[pokedex_id]
        formatted_id = f"{pokedex_id:04d}_{index:02d}"

        for files in os.listdir(SPRITES_DIR):
            if formatted_id in files:
                found_file = os.path.join(SPRITES_DIR, files)
                break

        return found_file

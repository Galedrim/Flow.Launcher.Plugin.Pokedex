import os

SPRITES_DIR  = r".\sprites"

class Sprites:

    def __init__(self):
        pass

    @staticmethod
    def get_icon(pokemon_id, region):

        found_file = None
        formatted_id = f"{pokemon_id:04d}"

        if region is not None:
            formatted_id = f"{pokemon_id:04d}_01"

        for files in os.listdir(SPRITES_DIR):
            if formatted_id in files:
                found_file = os.path.join(SPRITES_DIR, files)
                break
        return found_file
import os

SPRITES_DIR = r".\sprites"

class Sprite:
    
    index_map = {}
    
    @staticmethod
    def get_icon(pokemon_id):
        found_file = None
        formatted_id = f"{pokemon_id:04d}"

        if pokemon_id in Sprite.index_map:
            Sprite.index_map[pokemon_id] += 1
        else:
            Sprite.index_map[pokemon_id] = 0

        index = Sprite.index_map[pokemon_id]

        if index == 0:
            formatted_id = f"{pokemon_id:04d}"
        else:
            formatted_id = f"{pokemon_id:04d}_{index:02d}"

        for files in os.listdir(SPRITES_DIR):
            if formatted_id in files:
                found_file = os.path.join(SPRITES_DIR, files)
                break
                
        return found_file

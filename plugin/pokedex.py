import webbrowser
import json

from flox import Flox
from settings import Settings
from pokemon import Pokemon, Type, Nature, Ability

COUP_CRITIQUE_ICON = r".\images\coup_critique.png"
SMOGON_ICON = r".\images\smogon.png"
POKEBIP_ICON = r".\images\pokebip.png"
BULBAPEDIA_ICON = r".\images\bulbapedia.png"
PILULE_TALENT_ICON = r".\images\pilule_talent.png"

ABILITY_JSON_FILE = r".\data\ability.json"
REGIONAL_FORM_JSON_FILE = r".\data\regional_form.json"
NATURE_JSON_FILE = r".\data\nature.json"
POKEMON_JSON_FILE = r".\data\pokemon.json"
TYPE_JSON_FILE = r".\data\type.json"

class Pokedex(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = Settings.get_language()

        with open(TYPE_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.types_list = [Type(item) for item in data]

        with open(POKEMON_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.pokemons_list = [Pokemon(item) for item in data]

        with open(NATURE_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.natures_list = [Nature(item) for item in data]

        with open(ABILITY_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.abilities_list = [Ability(item) for item in data]

        with open(REGIONAL_FORM_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            for region, pokemons in data.items():
                for pokemon in pokemons.values():
                    if pokemon is not None:
                        regional_pokemon = Pokemon(pokemon, region)
                        self.pokemons_list.append(regional_pokemon)


    def results(self, query):

        for pokemon in self.pokemons_list:
            if self.language == "fr":
                if any(self.match(query, value) for value in [pokemon.name["fr"], pokemon.name["en"], pokemon.display_evolutions()]):
                    self.add_item(
                        title=f"{pokemon.display_name(self.language)} - {pokemon.display_types(self.types_list, self.language)}",
                        subtitle=f"{pokemon.display_evolutions()} - {pokemon.display_abilities()}\n{pokemon.display_stats()}",
                        icon=f"{pokemon.icon}",
                        context=pokemon.name,
                        method = self.open_url,
                        parameters=[f"https://www.coupcritique.fr/search/{pokemon.name['fr']}"]
                    )
            else:
                if self.match(query, pokemon.name['en']):
                    self.add_item(
                        title=f"{pokemon.display_name(self.language)} - {pokemon.display_types(self.types_list, self.language)}",
                        subtitle=f"{pokemon.display_stats()}",
                        icon=f"{pokemon.icon}",
                        context=pokemon.name,
                        method = self.open_url,
                        parameters=[f"https://bulbapedia.bulbagarden.net/wiki/{pokemon.name['en']}_(Pokémon)"]
                    )

        for nature in self.natures_list:
            if any(self.match(query, value) for value in [nature.name["fr"], nature.name["en"]]):
                self.add_item(
                    title=f"{nature.display_name(self.language)}",
                    subtitle=f"{nature.display_stats()}",
                )

        if self.language == "fr":
            for ability in self.abilities_list:
                if any(self.match(query, value) for value in [ability.name["fr"], ability.name["en"]]):
                    self.add_item(
                        title=f"{ability.display_name(self.language)}",
                        subtitle=f"{ability.display_description()}",
                        icon=PILULE_TALENT_ICON,
                        method=self.open_url,
                        parameters=[f"https://www.coupcritique.fr/search/{ability.name['fr']}"]
                    )

        return self._results

    def match(self, query, name):
        if query == "":
            return True

        q = query.lower()
        if q in name.lower():
            return True

    def context_menu(self, name):

        if self.language == "fr":
            self.add_item(
                title="Open Coupcritique.fr",
                subtitle="Open Coupcritique.fr",
                icon=COUP_CRITIQUE_ICON,
                method=self.open_url,
                parameters=[f"https://www.coupcritique.fr/search/{name['fr']}"]
            )
            self.add_item(
                title="Open Pokebip.com",
                subtitle="Open Pokebip",
                icon=POKEBIP_ICON,
                method=self.open_url,
                parameters=[f"https://www.pokebip.com/pokedex/pokemon/{name['fr']}"]
            )

        self.add_item(
            title="Open Smogon.com",
            subtitle="Open Smogon.com",
            icon=SMOGON_ICON,
            method=self.open_url,
            parameters=[f"https://www.smogon.com/dex/sv/pokemon/{name['en']}"]
        )

        self.add_item(
            title="Open Bulbapedia.com",
            subtitle="Open Bulbapedia.com",
            icon=BULBAPEDIA_ICON,
            method=self.open_url,
            parameters=[f"https://bulbapedia.bulbagarden.net/wiki/{name['en']}_(Pokémon)"]
        )

    def open_url(self, url):
        webbrowser.open(url)

    def query(self, query):
        self.results(query)

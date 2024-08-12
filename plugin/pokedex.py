import webbrowser

from flox import Flox
from settings import Settings

from plugin.abilities import AbilityLoader
from plugin.natures import NatureLoader
from plugin.pokemons import PokemonLoader
from plugin.types import TypeLoader

COUP_CRITIQUE_ICON = r".\images\coup_critique.png"
SMOGON_ICON = r".\images\smogon.png"
POKEBIP_ICON = r".\images\pokebip.png"
BULBAPEDIA_ICON = r".\images\bulbapedia.png"
PILULE_TALENT_ICON = r".\images\pilule_talent.png"

class Pokedex(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = Settings.get_language()

        self.pokemon_loader = PokemonLoader()
        self.nature_loader = NatureLoader()
        self.ability_loader = AbilityLoader()
        self.type_loader = TypeLoader()

    def results(self, query):

        language_used = self.language

        for pokemon in self.pokemon_loader.pokemon_list:
                if any(self.match(query, name) for name in pokemon.name.values() if name):
                    self.add_item(
                        title=f"{pokemon.get_name(language_used)} - {pokemon.get_types(language_used)}",
                        subtitle=f"{pokemon.get_evolutions(language_used)} - {pokemon.get_abilities(language_used)}\n{pokemon.get_stats()}",
                        icon=f"{pokemon.get_icon()}",
                        context=pokemon.name,
                        method=self.open_url,
                        parameters=[self.get_pokemon_url(pokemon.name)]
                    )

        for name_fr, nature in self.nature_loader.nature_dict.items():
            if any(self.match(query, name) for name in nature.name.values() if name):
                self.add_item(
                    title=f"{nature.get_name(language_used)}",
                    subtitle=f"{nature.get_stats()}",
                )

        for name_en, ability in self.ability_loader.ability_dict_en.items():
            if any(self.match(query, name) for name in ability.name.values() if name):
                self.add_item(
                    title=f"{ability.get_name(language_used)}",
                    subtitle=f"{ability.get_description(language_used)}",
                    icon=PILULE_TALENT_ICON,
                    method=self.open_url,
                    parameters=[self.get_ability_url(ability.name)]
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

    def get_pokemon_url(self, pokemon_name):

        if pokemon_name is not None:
            if self.language == 'fr': 
                return f"https://www.coupcritique.fr/search/{pokemon_name['fr']}"
            else:
                return f"https://bulbapedia.bulbagarden.net/wiki/{pokemon_name['en']}_(Pokémon)"
        return ''

    def get_ability_url(self, ability_name):

        if ability_name is not None:
            if self.language == 'fr': 
                return f"https://www.coupcritique.fr/search/{ability_name['fr']}"
            else:
                return f"https://bulbapedia.bulbagarden.net/wiki/{ability_name['en']}_(Ability)"
        return ''

    def query(self, query):
        self.results(query)

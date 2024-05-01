import webbrowser

from flox import Flox

from settings import Settings
from apiPokemon import ApiPokemon
from sprites import Sprites

COUP_CRITIQUE_ICON = ".\Images\coup_critique.png"
SMOGON_ICON = ".\Images\smogon.png"

class Pokedex(Flox):

    def results(self, query):
        self.language = Settings.get_language()
        if(self.language == "fr"):
            for pokemon in ApiPokemon.get_database():
                pokemon_name_FR = ApiPokemon.get_name_FR(pokemon)
                pokemon_name_EN = ApiPokemon.get_name_EN(pokemon)
                if self.match(query, pokemon_name_FR) or self.match(query, pokemon_name_EN):
                    self.add_item(
                        title=f"{pokemon_name_FR} / {pokemon_name_EN} {ApiPokemon.get_evolution(pokemon)}",
                        subtitle=f'{ApiPokemon.get_types_FR(pokemon)} -- {ApiPokemon.get_abilities(pokemon)}\n{ApiPokemon.get_stats(pokemon)}',
                        icon=Sprites.get_file(pokemon_name_EN),
                        context=f"{pokemon_name_FR} / {pokemon_name_EN}",
                        method = self.open_url,
                        parameters=[f"https://www.coupcritique.fr/search/{pokemon_name_FR}"]
                    )
        else:
            for pokemon in ApiPokemon.get_database():
                pokemon_name_EN = ApiPokemon.get_name_EN(pokemon)
                if self.match(query, pokemon_name_EN):
                    self.add_item(
                        title=f"{pokemon_name_EN}",
                        subtitle=f'{ApiPokemon.get_types_EN(pokemon)}\n{ApiPokemon.get_stats(pokemon)}',
                        icon=Sprites.get_file(pokemon_name_EN),
                        context=f"{pokemon_name_EN}",
                        method = self.open_url,
                        parameters=[f"https://www.smogon.com/dex/sv/pokemon/{pokemon_name_EN}"]
                    )
        return self._results

    def match(self, query, name):
        if name == "MissingNo.":
            return False

        if query == '':
            return True
        q = query.lower()

        if q in name.lower():
            return True

    def context_menu(self):
        if(self.language == "fr"):
            self.add_item(
                title='Open Coupcritique.fr',
                subtitle='Open Coupcritique.fr',
                icon=COUP_CRITIQUE_ICON,
                method=self.open_url,
                parameters=['https://www.coupcritique.fr/entity/pokemons']
            )

        self.add_item(
            title='Open Smogon.com',
            subtitle='Open Smogon.com',
            icon=SMOGON_ICON,
            method=self.open_url,
            parameters=['https://www.smogon.com/dex/sv/pokemon/']
        )

    def open_url(self, url):
        webbrowser.open(url)

    def query(self, query):
        self.results(query)

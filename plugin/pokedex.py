import webbrowser

from flox import Flox

from settings import Settings
from apiPokemon import ApiPokemon
from sprites import Sprites

COUP_CRITIQUE_ICON = ".\\Images\\coup_critique.png"
SMOGON_ICON = ".\\Images\\smogon.png"
POKEBIP_ICON = ".\\Images\\pokebip.png"
BULBAPEDIA_ICON = ".\\Images\\bulbapedia.png"

class Pokedex(Flox):

    def results(self, query):
        self.language = Settings.get_language()
        for pokemon in ApiPokemon.get_database():
            pokemon_name = ApiPokemon.get_names(pokemon)
            if(self.check(pokemon_name['en'])):
                if(self.language == "fr"):
                        if any(self.match(query, value) for value in [pokemon_name['fr'], pokemon_name['en'], ApiPokemon.get_evolution(pokemon)]):
                                self.add_item(
                                    title=f"{pokemon_name['fr']} / {pokemon_name['en']} {ApiPokemon.get_types(pokemon)}",
                                    subtitle=f'{ApiPokemon.get_evolution(pokemon)} {ApiPokemon.get_abilities(pokemon)}\n{ApiPokemon.get_stats(pokemon)}',
                                    icon=Sprites.get_file(pokemon_name['en']),
                                    context=pokemon_name,
                                    method = self.open_url,
                                    parameters=[f"https://www.pokebip.com/pokedex/pokemon/{pokemon_name['fr']}"]
                                )
                else:
                    if self.match(query, pokemon_name['en']):
                        self.add_item(
                            title=f"{pokemon_name['en']} {ApiPokemon.get_types(pokemon)}",
                            subtitle=f'{ApiPokemon.get_stats(pokemon)}',
                            icon=Sprites.get_file(pokemon_name['en']),
                            context=pokemon_name,
                            method = self.open_url,
                            parameters=[f"https://bulbapedia.bulbagarden.net/wiki/{pokemon_name['en']}_(Pokémon)"]
                        )
        return self._results

    def match(self, query, name):
        if query == '':
            return True

        q = query.lower()
        if q in name.lower():
            return True

    def check(self, name):
        if name == 'MissingNo.':
            return False
        return True

    def context_menu(self, names):
        self.language = Settings.get_language()
        pokemon_name_en = names['en']

        if(self.language == "fr"):
            pokemon_name_fr = names['fr']
            self.add_item(
                title='Open Coupcritique.fr',
                subtitle='Open Coupcritique.fr',
                icon=COUP_CRITIQUE_ICON,
                method=self.open_url,
                parameters=[f'https://www.coupcritique.fr/search/{pokemon_name_fr}']
            )
            self.add_item(
                title="Open Pokebip.com",
                subtitle="Open Pokebip",
                icon=POKEBIP_ICON,
                method=self.open_url,
                parameters=[f'https://www.pokebip.com/pokedex/pokemon/{pokemon_name_fr}']
            )

        self.add_item(
                title='Open Smogon.com',
                subtitle='Open Smogon.com',
                icon=SMOGON_ICON,
                method=self.open_url,
                parameters=[f'https://www.smogon.com/dex/sv/pokemon/{pokemon_name_en}']
            )
        
        self.add_item(
                title='Open Bulbapedia.com',
                subtitle='Open Bulbapedia.com',
                icon=BULBAPEDIA_ICON,
                method=self.open_url,
                parameters=[f"https://bulbapedia.bulbagarden.net/wiki/{pokemon_name_en}_(Pokémon)"]
            )

    def open_url(self, url):
        webbrowser.open(url)

    def query(self, query):
        self.results(query)

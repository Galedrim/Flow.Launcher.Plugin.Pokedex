import webbrowser

from flox import Flox
from settings import Settings

from plugin.abilities import AbilityLoader
from plugin.natures import NatureLoader
from plugin.pokemons import PokemonLoader

BULBAPEDIA_ICON = r".\images\bulbapedia.png"
COUP_CRITIQUE_ICON = r".\images\coup_critique.png"
PILULE_TALENT_ICON = r".\images\pilule_talent.png"
POKEBIP_ICON = r".\images\pokebip.png"
SEREBII_ICON = r".\images\serebii.png"
SMOGON_ICON = r".\images\smogon.png"

class Pokedex(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = Settings.get_language()

        self.pokemon_loader = PokemonLoader()
        self.nature_loader = NatureLoader()
        self.ability_loader = AbilityLoader()

    def results(self, query):

        self.pokemon_base_results(query)
        self.pokemon_regional_results(query)
        self.pokemon_mega_results(query)
        self.pokemon_nature_results(query)
        self.pokemon_ability_results(query)

        return self._results

    def pokemon_base_results(self, query):
        for name, pokemon in self.pokemon_loader.pokemon_base_dict.items():
            if self.language == 'fr':
                all_names = list(pokemon.name.values())
                for pre_evolution in pokemon.pre_evolutions.values():
                    all_names.extend(pre_evolution)
    
                for next_evolution in pokemon.next_evolutions.values():
                    all_names.extend(next_evolution)

                if any(self.match(query, name) for name in all_names if name):
                    self.add_pokemon_item(pokemon, pokemon.name['fr'])
            else:
                all_names = [pokemon.name['en'].lower()]
                for pre_evolution in pokemon.pre_evolutions['en']:
                    all_names.append(pre_evolution.lower())

                for next_evolution in pokemon.next_evolutions['en']:
                    all_names.append(next_evolution.lower())

                if any(self.match(query, name) for name in all_names if name):
                    self.add_pokemon_item(pokemon, pokemon.name['en'])

    def pokemon_regional_results(self, query):
        for name, pokemon in self.pokemon_loader.pokemon_regional_dict.items():
            if self.language == 'fr': 
                all_names = list(pokemon.name.values())
                for pre_evolution in pokemon.pre_evolutions.values():
                    all_names.extend(pre_evolution)
    
                for next_evolution in pokemon.next_evolutions.values():
                    all_names.extend(next_evolution)

                if any(self.match(query, name) for name in all_names if name):
                    self.add_pokemon_item(pokemon, pokemon.name['fr'])

            else:
                all_names = [pokemon.name['en'].lower()]
                for pre_evolution in pokemon.pre_evolutions['en']:
                    all_names.append(pre_evolution.lower())

                for next_evolution in pokemon.next_evolutions['en']:
                    all_names.append(next_evolution.lower())   

                if any(self.match(query, name) for name in all_names if name):
                    self.add_pokemon_item(pokemon, pokemon.base_forms['en'])

    def pokemon_mega_results(self, query):
        for name, pokemon in self.pokemon_loader.pokemon_mega_dict.items():
            if self.language == 'fr': 
                all_names = list(pokemon.name.values())
                for pre_evolution in pokemon.pre_evolutions.values():
                    all_names.extend(pre_evolution)

                if any(self.match(query, name) for name in all_names if name):
                    self.add_pokemon_item(pokemon, pokemon.name['fr'])

            else:
                all_names = [pokemon.name['en'].lower()]
                for pre_evolution in pokemon.pre_evolutions['en']:
                    all_names.append(pre_evolution.lower())

                if any(self.match(query, name) for name in all_names if name):
                    self.add_pokemon_item(pokemon, pokemon.pre_evolutions['en'][0].lower())
    
    def pokemon_nature_results(self, query):
        for name, nature in self.nature_loader.nature_dict.items():
            if any(self.match(query, name) for name in nature.name.values()):
                self.add_item(
                    title=f"{nature.get_name(self.language)}",
                    subtitle=f"{nature.get_stats()}",
                )

    def pokemon_ability_results(self, query):
        for name, ability in self.ability_loader.ability_dict_en.items():
            if any(self.match(query, name) for name in ability.name.values()):
                if self.language == 'fr': 
                    self.add_ability_item(ability, ability.name['fr'].lower())
                else:
                    self.add_ability_item(ability, ability.name['en'].lower())

    def add_pokemon_item(self, pokemon, pokemon_url):
        self.add_item(
            title=f"{pokemon.get_name(self.language)} - {pokemon.get_types(self.language)}",
            subtitle=f"{pokemon.get_evolutions(self.language)} - {pokemon.get_abilities(self.language)}\n{pokemon.get_stats(self.language)}",
            icon=f"{pokemon.get_icon()}",
            context=pokemon.name,
            method=self.open_url,
            parameters=[self.get_pokemon_url(pokemon_url)]
        )

    def add_ability_item(self, ability, ability_url):
        self.add_item(
            title=f"{ability.get_name(self.language)}",
            subtitle=f"{ability.get_description(self.language)}",
            icon=PILULE_TALENT_ICON,
            method=self.open_url,
            parameters=[self.get_ability_url(ability_url)]
        )

    def match(self, query, name):
        if query == "":
            return True

        q = query.lower()

        if q in name.lower():
            return True

    def context_menu(self, name):

        if self.language == "fr":
            self.add_item(
                title="Open Pokebip.com",
                subtitle="Open Pokebip",
                icon=POKEBIP_ICON,
                method=self.open_url,
                parameters=[f"https://www.pokebip.com/pokedex/pokemon/{name['fr']}"]
            )
            self.add_item(
                title="Open Coupcritique.fr",
                subtitle="Open Coupcritique.fr",
                icon=COUP_CRITIQUE_ICON,
                method=self.open_url,
                parameters=[f"https://www.coupcritique.fr/search/{name['fr']}"]
            )


        self.add_item(
            title="Open Serebii.com",
            subtitle="Open Serebii.com",
            icon=SEREBII_ICON,
            method=self.open_url,
            parameters=[f"https://www.serebii.net/pokemon/{name['en']}"]
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
                return f"https://www.pokebip.com/pokedex/pokemon/{pokemon_name}"
            else:
                return f"https://www.serebii.net/pokemon/{pokemon_name}"
        return ''

    def get_ability_url(self, ability_name):

        if ability_name is not None:
            if self.language == 'fr': 
                return f"https://www.pokebip.com/pokedex/talents/{ability_name}"
            else:
                return f"https://www.serebii.net/abilitydex/{ability_name}.shtml"
        return ''

    def query(self, query):
        self.results(query)

import webbrowser

from flox import Flox
from typing import List, Dict

from settings import Settings

from infos.pokemon_sprites import Sprite
from infos.pokemon_abilities import AbilityLoader, Ability
from infos.pokemon_natures import NatureLoader, Nature
from infos.pokemon_types import TypeLoader

from pokemons.pokemons import Pokemon, Evolutions
from pokemons.nationals import PokemonNationalLoader
from pokemons.regionals import PokemonRegionalLoader
from pokemons.megas import PokemonMegaLoader, PokemonToMega, MegaEvolution

PILULE_TALENT_ICON = r".\images\pilule_talent.png"

BULBAPEDIA_ICON = r".\images\website\bulbapedia.png"
COUP_CRITIQUE_ICON = r".\images\website\coup_critique.png"
POKEBIP_ICON = r".\images\website\pokebip.png"
SEREBII_ICON = r".\images\website\serebii.png"
SMOGON_ICON = r".\images\website\smogon.png"

DEFAULT_WEBSITE = 'bulbapedia'
VALID_WEBSITES = {'bulbapedia', 'coup-critique', 'pokebip', 'serebii', 'smogon'}

LANGUAGE_KEYS = {
    'fr': ['fr', 'en'], 
    'en': ['en']
}
POKEMON_STAT_LABELS = {
    'fr': {'hp': 'PV', 'atk': 'Atq', 'def': 'Def', 'spe_atk': 'Atq Spe', 'spe_def': 'Def Spe', 'spd': 'Vit'},
    'en': {'hp': 'HP','atk': 'Atk', 'def': 'Def', 'spe_atk': 'Atk Spe', 'spe_def': 'Def Spe', 'spd': 'Spe'}
}
NATURE_STAT_LABELS = {
    'fr': {'atk': 'Atq', 'def': 'Def', 'spe_atk': 'Atq Spe', 'spe_def': 'Def Spe', 'spd': 'Vit'},
    'en': {'atk': 'Atk', 'def': 'Def', 'spe_atk': 'Atk Spe', 'spe_def': 'Def Spe', 'spd': 'Spe'}
}

class Pokedex(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        website = self.settings.get('default_website', DEFAULT_WEBSITE)
        if website in VALID_WEBSITES:
            self.default_website = website
        else:
            self.default_website = DEFAULT_WEBSITE
        self.language = Settings.get_language()

        self.pokemon_national_loader = PokemonNationalLoader()
        self.pokemon_regional_loader = PokemonRegionalLoader()
        self.pokemon_mega_loader = PokemonMegaLoader()

        self.nature_loader = NatureLoader()
        self.type_loader = TypeLoader()
        self.ability_loader = AbilityLoader()

    def results(self, query: str):

        self.pokemons_nationals_results(query)
        self.pokemons_regionals_results(query)
        self.pokemons_mega_results(query)
        self.pokemon_natures_results(query)
        self.pokemon_abilities_results(query)

        return self._results

# ###############
# POKEMON
# ###############
    def _get_pokemon_comparable_names(self, pokemon: Pokemon) -> List[str]:
        keys_to_compare = LANGUAGE_KEYS[self.language]

        if not pokemon.evolutions:
            return [pokemon.name.get(key, "").lower() for key in keys_to_compare]

        if pokemon.evolutions:
            pre_evolutions_names = self._get_evolution_names(pokemon.evolutions.pre)
            next_evolutions_names = self._get_evolution_names(pokemon.evolutions.next)

        pokemon_names = []
        for key in keys_to_compare:
            pokemon_names.append(pokemon.name.get(key, ""))
            pokemon_names.extend(pre_evolutions_names.get(key, ""))
            pokemon_names.extend(next_evolutions_names.get(key, ""))
        return [pokemon_names]

    def _get_pokemon_title(self, pokemon: Pokemon) -> str:
        pokedex_id = f"#{pokemon.pokedex_id:04d}"
        names = self.dump_pokemon_names(pokemon.name)
        types = self.dump_pokemon_types(pokemon.types)

        return f"{pokedex_id}: {names} - {types}"

    def dump_pokemon_names(self, pokemon_name: Dict) -> str:
        keys_to_compare = LANGUAGE_KEYS[self.language]
        pokemon_names = [pokemon_name.get(key) for key in keys_to_compare]
        return " | ".join(pokemon_names).strip()

    def dump_pokemon_types(self, pokemon_types: List) -> str:
        types_names = [type_obj['name'] for type_obj in pokemon_types]
        types_obj = [self.type_loader._get_type(type_name) for type_name in types_names]
        completed_types = [f"{types.emoji} {types.name.get(self.language)}" for types in types_obj]
        return " | ".join(completed_types).strip()

    def _get_pokemon_subtitle(self, pokemon: Pokemon) -> str:
        abilities = self.dump_pokemon_abilities(pokemon.abilities)
        stats = self.dump_pokemon_stats(pokemon.stats)
        evolutions = self.dump_pokemon_evolutions(pokemon.evolutions)

        return f"{evolutions} - {abilities}\n{stats}"

    def dump_pokemon_abilities(self, pokemon_abilities: List) -> str:
        abilities_names = [ability_obj['name'] for ability_obj in pokemon_abilities]
        abilities_obj = [self.ability_loader._get_ability(ability_name) for ability_name in abilities_names]
        completed_abilities = [f"{ability.name.get(self.language)}" for ability in abilities_obj]
        return " | ".join(completed_abilities).strip()

    def dump_pokemon_stats(self, pokemon_stats: Dict) -> str:
        stat_values = []
        for stat, value in pokemon_stats.items():
            stat_values.append(f"{POKEMON_STAT_LABELS[self.language][stat]}: {value}")
        return " | ".join(stat_values)

    def dump_pokemon_evolutions(self, pokemon_evolutions: Evolutions) -> str:
        if not pokemon_evolutions:
            return "X"

        pre_evolutions_names = self._get_evolution_names(pokemon_evolutions.pre)
        next_evolutions_names = self._get_evolution_names(pokemon_evolutions.next)

        pre_evolutions = " > ".join(pre_evolutions_names.get(self.language)) if pre_evolutions_names else ''
        next_evolutions = " > ".join(next_evolutions_names.get(self.language)) if next_evolutions_names else ''

        if pre_evolutions and next_evolutions:
            return f"{pre_evolutions} > X > {next_evolutions}"
        elif pre_evolutions:
            return f"{pre_evolutions} > X"
        elif next_evolutions:
            return f"X > {next_evolutions}"
        else:
            return "X"

    def _get_evolution_names(self, pokemon_evolutions: Dict) -> Dict:
        evolution_names = {
            'fr': [],
            'en': []
        }
        pokemons = self.pokemon_national_loader._get_pokemons()
        if pokemon_evolutions:
            for evolution in pokemon_evolutions:
                pokemon = pokemons.get(evolution.get('pokedex_id'))
                name_fr = pokemon.name.get('fr')
                name_en = pokemon.name.get('en')

                if name_fr:
                    evolution_names['fr'].append(name_fr)
                if name_en:
                    evolution_names['en'].append(name_en)

        return evolution_names

# ###############
# POKEMON NATIONALS
# ###############
    def pokemons_nationals_results(self, query: str):
        pokemons = self.pokemon_national_loader._get_pokemons()
        for national_id, pokemon in pokemons.items():
            comparable_names = self._get_pokemon_comparable_names(pokemon)
            if any(self.match(query, str(name)) for name in comparable_names):
                urls = self._get_pokemon_nationals_urls(pokemon)
                default_url = urls.get(self.default_website) or urls.get(DEFAULT_WEBSITE)
                self.add_item(
                    title=self._get_pokemon_title(pokemon),
                    subtitle=self._get_pokemon_subtitle(pokemon),
                    icon=self._get_pokemon_nationals_icon(pokemon),
                    context=urls,
                    method=self.open_url,
                    parameters=[default_url]
                )

    def _get_pokemon_nationals_icon(self, pokemon_national: Pokemon) -> str:
        return Sprite._get_basic_icon(pokemon_national.pokedex_id)

    def _get_pokemon_nationals_urls(self, pokemon_national: Pokemon) -> Dict[str, str]:
        urls = {}
        for website in VALID_WEBSITES:
            if website == "bulbapedia":
                pokemon_name = pokemon_national.name['en'].lower()
                urls[website] = f"https://bulbapedia.bulbagarden.net/wiki/{pokemon_name}_(Pokémon)"
            elif website == "coup-critique":
                pokemon_name = pokemon_national.name['fr'].lower()
                urls[website] = f"https://www.coupcritique.fr/search/{pokemon_name}"
            elif website == "pokebip":
                pokemon_name = pokemon_national.name['fr'].lower()
                urls[website] = f"https://www.pokebip.com/pokedex/pokemon/{pokemon_name}"
            elif website == "serebii":
                pokemon_name = pokemon_national.name['en'].lower()
                urls[website] = f"https://www.serebii.net/pokemon/{pokemon_name}"
            elif website == "smogon":
                pokemon_name = pokemon_national.name['en'].lower()
                urls[website] = f"https://www.smogon.com/dex/sv/pokemon/{pokemon_name}"
            else:
                raise ValueError('Invalid website')
        return urls

# ###############
# REGIONAL REGIONALS
# ###############
    def pokemons_regionals_results(self, query: str):
        pokemons = self.pokemon_regional_loader._get_pokemons()
        for regional_id, pokemon in pokemons.items():
            comparable_names = self._get_pokemon_comparable_names(pokemon)
            if any(self.match(query, str(name)) for name in comparable_names):
                urls = self._get_pokemon_regionals_urls(pokemon)
                default_url = urls.get(self.default_website) or urls.get(DEFAULT_WEBSITE)
                self.add_item(
                    title=self._get_pokemon_title(pokemon),
                    subtitle=self._get_pokemon_subtitle(pokemon),
                    icon=self._get_pokemon_regionals_icon(pokemon),
                    context=urls,
                    method=self.open_url,
                    parameters=[default_url]
                )

    def _get_pokemon_regionals_icon(self, pokemon_regional: Pokemon) -> str:
        return Sprite._get_variant_icon(pokemon_regional.pokedex_id)

    def _get_pokemon_regionals_urls(self, pokemon_regional: Pokemon) -> Dict[str, str]:
        pokemons_nationals = self.pokemon_national_loader._get_pokemons()
        pokemon_national = pokemons_nationals.get(str(pokemon_regional.pokedex_id))

        urls = {}
        for website in VALID_WEBSITES:
            if website == "bulbapedia":
                pokemon_name = pokemon_national.name['en'].lower()
                urls[website] = f"https://bulbapedia.bulbagarden.net/wiki/{pokemon_name}_(Pokémon)"
            elif website == "coup-critique":
                pokemon_name = pokemon_regional.name['fr'].lower()
                urls[website] = f"https://www.coupcritique.fr/search/{pokemon_name}"
            elif website == "pokebip":
                pokemon_name = pokemon_regional.name['fr'].lower()
                urls[website] = f"https://www.pokebip.com/pokedex/pokemon/{pokemon_name}"
            elif website == "serebii":
                pokemon_name = pokemon_regional.name['en'].lower()
                urls[website] = f"https://www.serebii.net/pokemon/{pokemon_name}"
            elif website == "smogon":
                pokemon_name = pokemon_regional.name['en'].lower()
                urls[website] = f"https://www.smogon.com/dex/sv/pokemon/{pokemon_name}"
            else:
                raise ValueError('Invalid website')
        return urls

# ###############
# POKEMON MEGAS
# ###############
    def pokemons_mega_results(self, query: str):
        pokemons = self.pokemon_mega_loader._get_pokemons()
        for megas_id, pokemon in pokemons.items():
            for mega in pokemon.formes:
                comparable_names = self._get_mega_comparable_names(mega)
                if any(self.match(query, str(name)) for name in comparable_names):
                    urls = self._get_pokemon_mega_urls(pokemon)
                    default_url = urls.get(self.default_website) or urls.get(DEFAULT_WEBSITE)
                    self.add_item(
                        title=self._get_mega_title(pokemon, mega),
                        subtitle=self._get_mega_subtitle(pokemon, mega),
                        icon=self._get_pokemon_mega_icon(pokemon),
                        context=urls,
                        method=self.open_url,
                        parameters=[default_url]
                    )

    def _get_mega_comparable_names(self, mega: MegaEvolution) -> List[str]:
        keys_to_compare = LANGUAGE_KEYS[self.language]
        return [mega.name.get(key, "").lower() for key in keys_to_compare]

    def _get_mega_title(self, pokemon: PokemonToMega, mega: MegaEvolution) -> str:
        pokedex_id = f"#{pokemon.pokedex_id:04d}"
        names = self.dump_pokemon_names(mega.name)
        types = self.dump_pokemon_types(mega.types)
        return f"{pokedex_id}: {names} - {types}"

    def _get_mega_subtitle(self, pokemon: PokemonToMega, mega: MegaEvolution) -> str:
        abilities = self.dump_pokemon_abilities(mega.abilities)
        stats = self.dump_pokemon_stats(mega.stats)
        pokemon = pokemon.name.get(self.language)
        return f"{pokemon} > X - {abilities}\n{stats}"

    def _get_pokemon_mega_icon(self, pokemon: PokemonToMega) -> str:
        return Sprite._get_variant_icon(pokemon.pokedex_id)

    def _get_pokemon_mega_urls(self, pokemon: PokemonToMega) -> Dict[str, str]:
        urls = {}
        for website in VALID_WEBSITES:
            if website == "bulbapedia":
                pokemon_name = pokemon.name['en'].lower()
                urls[website] = f"https://bulbapedia.bulbagarden.net/wiki/{pokemon_name}_(Pokémon)"
            elif website == "coup-critique":
                pokemon_name = pokemon.name['fr'].lower()
                urls[website] = f"https://www.coupcritique.fr/search/{pokemon_name}"
            elif website == "pokebip":
                pokemon_name = pokemon.name['fr'].lower()
                urls[website] = f"https://www.pokebip.com/pokedex/pokemon/{pokemon_name}"
            elif website == "serebii":
                pokemon_name = pokemon.name['en'].lower()
                urls[website] = f"https://www.serebii.net/pokemon/{pokemon_name}"
            elif website == "smogon":
                pokemon_name = pokemon.name['en'].lower()
                urls[website] = f"https://www.smogon.com/dex/sv/pokemon/{pokemon_name}"
            else:
                raise ValueError('Invalid website')
        return urls

# ###############
# POKEMON NATURE
# ###############
    def pokemon_natures_results(self, query: str):
        natures = self.nature_loader._get_natures()
        for nature in natures:
            comparable_names = self._get_nature_comparable_names(nature)
            if any(self.match(query, str(name)) for name in comparable_names):
                urls = self._get_nature_urls()
                default_url = urls.get(self.default_website) or urls.get(DEFAULT_WEBSITE)
                self.add_item(
                    title=self._get_nature_title(nature),
                    subtitle=self._get_nature_subtitle(nature),
                    context=urls,
                    method=self.open_url,
                    parameters=[default_url]
                )

    def _get_nature_comparable_names(self, nature: Nature) -> List[str]:
        keys_to_compare = LANGUAGE_KEYS[self.language]
        return [nature.name.get(key, "") for key in keys_to_compare]

    def _get_nature_title(self, nature: Nature) -> str:
        keys_to_compare = LANGUAGE_KEYS[self.language]
        values = [nature.name.get(key, "") for key in keys_to_compare]
        return " | ".join(values)  

    def _get_nature_subtitle(self, nature: Nature) -> str:
        stat_values = []
        for stat, value in nature.stats.items():
            if value: 
                stat_values.append(f"{NATURE_STAT_LABELS[self.language][stat]}: {value}")
        return " | ".join(stat_values) if stat_values else 'X'
    
    def _get_nature_urls(self) -> Dict[str, str]:
        urls = {}
        for website in VALID_WEBSITES:
            if website == "bulbapedia":
                urls[website] = "https://bulbapedia.bulbagarden.net/wiki/Nature"
            elif website == "coup-critique":
                urls[website] = ""
            elif website == "pokebip":
                urls[website] = "https://www.pokebip.com/page/jeuxvideo/natures"
            elif website == "serebii":
                urls[website] = "https://www.serebii.net/games/natures.shtml"
            elif website == "smogon":
                urls[website] = ""
            else:
                raise ValueError('Invalid website')
        return urls

###############
# POKEMON ABILITY
###############
    def pokemon_abilities_results(self, query: str):
        abilities = self.ability_loader._get_abilities()
        for ability in abilities:
            comparable_names = self._get_ability_comparable_names(ability)
            if any(self.match(query, str(name)) for name in comparable_names):
                urls = self._get_ability_urls(ability)
                default_url = urls.get(self.default_website)
                self.add_item(
                    title=self._get_ability_title(ability),
                    subtitle=self._get_ability_subtitle(ability),
                    icon=PILULE_TALENT_ICON,
                    context=urls,
                    method=self.open_url,
                    parameters=[default_url]
                )

    def _get_ability_comparable_names(self, ability: Ability) -> List[str]:
        keys_to_compare = LANGUAGE_KEYS[self.language]
        return [ability.name.get(key, "") for key in keys_to_compare]

    def _get_ability_title(self, ability: Ability) -> str:
        keys_to_compare = LANGUAGE_KEYS[self.language]
        values = [ability.name.get(key, "") for key in keys_to_compare]
        return " | ".join(values)  

    def _get_ability_subtitle(self, ability: Ability) -> str:
        keys_to_compare = LANGUAGE_KEYS[self.language]
        values = [ability.description.get(key, "") for key in keys_to_compare] 
        return " | ".join(values)  
    
    def _get_ability_urls(self, ability: Ability) -> Dict[str, str]:
        urls = {}
        for website in VALID_WEBSITES:
            if website == "bulbapedia":
                ability_name = ability.name['en']
                urls[website] = f"https://bulbapedia.bulbagarden.net/wiki/{ability_name}_(Ability)"
            elif website == "coup-critique":
                ability_name = ability.name['fr']
                urls[website] = f"https://www.coupcritique.fr/search/{ability_name}"
            elif website == "pokebip":
                ability_name = ability.name['fr']
                urls[website] = f"https://www.pokebip.com/pokedex/talents/{ability_name}"
            elif website == "serebii":
                ability_name = ability.name['en'].lower().replace(' ', '')
                urls[website] = f"https://www.serebii.net/abilitydex/{ability_name}.shtml"
            elif website == "smogon":
                ability_name = ability.name['en']
                urls[website] = f"https://www.smogon.com/dex/sv/abilities/{ability_name}"
            else:
                raise ValueError('Invalid website')
        return urls

# ###############
# POKEMON QUERY
# ###############
    def match(self, query: str, name: str):
        if query == "":
            return True
        q = query.lower()

        if q in name.lower():
            return True

    def query(self, query: str):
        self.results(query)

# ###############
# POKEMON URLS
# ###############
    def context_menu(self, urls: Dict[str, str]):
        for website, url in urls.items():
            if url:
                match website:
                    case "bulbapedia":
                        self.add_item(
                            title="Open Bulbapedia.com",
                            subtitle="Open Bulbapedia.com",
                            icon=BULBAPEDIA_ICON,
                            method=self.open_url,
                            parameters=[url]
                        )
                    case "coup-critique":
                        self.add_item(
                            title="Open Coupcritique.fr",
                            subtitle="Open Coupcritique.fr",
                            icon=COUP_CRITIQUE_ICON,
                            method=self.open_url,
                            parameters=[url]
                        )
                    case "pokebip":
                        self.add_item(
                            title="Open Pokebip.com",
                            subtitle="Open Pokebip",
                            icon=POKEBIP_ICON,
                            method=self.open_url,
                            parameters=[url]
                        )
                    case "serebii":
                        self.add_item(
                            title="Open Serebii.com",
                            subtitle="Open Serebii.com",
                            icon=SEREBII_ICON,
                            method=self.open_url,
                            parameters=[url]
                        )
                    case "smogon":
                        self.add_item(
                            title="Open Smogon.com",
                            subtitle="Open Smogon.com",
                            icon=SMOGON_ICON,
                            method=self.open_url,
                            parameters=[url]
                        )
                    case _:
                        raise ValueError(f"Unknown website: {website}")

    def open_url(self, url: str):
        webbrowser.open(url)

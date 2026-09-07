from team import PokemonTeam
from pokemon import Pokemon
from pokeapi import search_by_name, get_stats

TYPE_WEAKNESSES = {
    "normal": ["fighting"],
    "fire": ["water", "ground", "rock"],
    "water": ["electric", "grass"],
    "electric": ["ground"],
    "grass": ["fire", "ice", "poison", "flying", "bug"],
    "ice": ["fire", "fighting", "rock", "steel"],
    "fighting": ["flying", "psychic", "fairy"],
    "poison": ["ground", "psychic"],
    "ground": ["water", "grass", "ice"],
    "flying": ["electric", "ice", "rock"],
    "psychic": ["bug", "ghost", "dark"],
    "bug": ["fire", "flying", "rock"],
    "rock": ["water", "grass", "fighting", "ground", "steel"],
    "ghost": ["ghost", "dark"],
    "dragon": ["ice", "dragon", "fairy"],
    "dark": ["fighting", "bug", "fairy"],
    "steel": ["fire", "fighting", "ground"],
    "fairy": ["poison", "steel"],
}

def run_option_1(team: PokemonTeam) -> None:
    pokemon_name = input("Enter a Pokemon Name: ")
    data = search_by_name(pokemon_name)

    if data is not None:
        stats = get_stats(data)
        print_stats(stats)
        answer = input(f"Would you like to add {pokemon_name} to your team? (y/n): ")

        if answer.strip().lower() == 'y':
            pokemon = create_pokemon(stats)

            if add_to_team(pokemon, team):
                print(f"{pokemon.name} was added to your team!")
                print(f"Team size: {team.size}/{team.limit}")
            else:
                print("Your team is already full!")

def add_to_team(pokemon: Pokemon, team) -> PokemonTeam:
    return team.add_pokemon(pokemon)

def create_pokemon(stats: dict) -> Pokemon:
    return Pokemon(
        name=stats["name"],
        id=stats["id"],
        types=stats["types"],
        height=stats["height"],
        weight=stats["weight"],
        base_stats=stats["base_stats"],
    )

def print_stats(stats: dict) -> None:
    print(f"Name: {stats["name"]}")
    print(f"Pokedex ID: {stats["id"]}")
    print(f"Type: ")
    print(f"Height: {stats["height"]} ft")
    print(f"Weight: {stats["weight"]} lbs")

from team import PokemonTeam
from pokemon import Pokemon
from pokeapi import search_by_name, get_stats
from database import save_team, load_team, get_team_names

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
    """Asks the user for a Pokémon name, looks up its info,
     and lets them decide if they want to add it to their team."""
    pokemon_name = input("Enter a Pokemon Name: ")
    print()
    data = search_by_name(pokemon_name)

    if data is not None:
        stats = get_stats(data)
        print_stats(stats)
        answer = input(f"Would you like to add {pokemon_name} to your team? (y/n): ")
        print()


        if answer.strip().lower() == 'y':
            pokemon = create_pokemon(stats)

            if add_to_team(pokemon, team):
                print(f"{pokemon.name} was added to your team!", end='\n\n')
                print(f"Team size: {team.size}/{team.limit}", end='\n\n')
            else:
                print("Your team is already full!", end='\n\n')
        else:
            print(f"{pokemon_name} was not added to your team.", end='\n\n')

def run_option_2(team: PokemonTeam) -> None:
    """Prints out the current lineup, showing each Pokémon's types and weight."""
    if team.size == 0:
        print("\nYour team is empty.")
        return

    print("\n================================")
    print("           YOUR TEAM")
    print("================================\n")

    for number, pokemon in enumerate(team.team, start=1):
        formatted_types = ", ".join(
            pokemon_type.title()
            for pokemon_type in pokemon.types
        )

        type_label = "Type" if len(pokemon.types) == 1 else "Types"

        print(f"{number}. {pokemon.name.title()}")
        print(f"   {type_label}: {formatted_types}")
        print(f"   Weight: {pokemon.weight} kg")
        print()

    print(f"Team size: {team.size}/{team.limit}")
    print("\n-------------------------------------", end= '\n\n')


def run_option_3(team: PokemonTeam) -> None:
    """Gives a quick rundown of the team's strengths and weaknesses, highlighting shared type vulnerabilities and who has the best stats."""
    if team.size == 0:
        print("Your team is empty.")
        return

    print("\n================================")
    print("         TEAM ANALYSIS")
    print("================================\n")

    print_shared_weaknesses(team)
    print_available_types(team)
    print_highest_stats(team)

    if team.size == team.limit:
        print("\nWarning:")
        print("Your team contains the maximum of six Pokémon.")
        print("Remove a Pokémon before adding another.")

    print("\n-------------------------------------", end='\n\n')

def run_option_4(team: PokemonTeam) -> None:
    """Lets the user pick a name and saves their current team to the database."""
    if team.size == 0:
        print("You cannot save an empty team.")
        return

    team_name = input("Enter a name for this team: ").strip()

    if not team_name:
        print("The team name cannot be empty.", end='\n\n')
        return

    save_team(team_name, team)
    print(f"{team_name} was saved successfully.", end='\n\n')

def run_option_5(team: PokemonTeam) -> PokemonTeam:
    """Shows a list of previously saved teams and lets the user pick one to load up."""
    teams = get_team_names()

    if not teams:
        print("There are no saved teams to load.", end='\n\n')
        return team

    print("\n================================")
    print(" SAVED TEAMS")
    print("================================\n")

    for num, name in enumerate(teams, start=1):
        print(f"{num}. {name}")
    print()

    choice = input("Enter the name of the team to load: ").strip()

    if choice not in teams:
        print("That is not a valid name.", end='\n\n')
        return team

    loaded_team = load_team(choice)

    if loaded_team is None:
        print("That team could not be found.", end='\n\n')
        return team

    print(f"Loaded team with {loaded_team.size} Pokémon.", end='\n\n')
    return loaded_team

def run_option_6(team: PokemonTeam) -> None:
    """Lets the user pick a Pokémon from their current lineup and removes it."""
    if team.size == 0:
        print("Your team is empty.", end='\n\n')
        return

    print("\n================================")
    print(" EDIT TEAM")
    print("================================\n")

    for number, pokemon in enumerate(team.team, start=1):
        print(f"{number}. {pokemon.name.title()}")
    print()

    choice = input("Enter the number of the Pokémon to remove (or 0 to cancel): ").strip()

    if choice == '0':
        print("No changes made.", end='\n\n')
        return

    if not choice.isdigit():
        print("That is not a valid number.", end='\n\n')
        return

    removed = team.remove_pokemon(int(choice))

    if removed is None:
        print("That is not a valid Pokémon number.", end='\n\n')
        return

    print(f"{removed.name.title()} was removed from your team.", end='\n\n')
    print(f"Team size: {team.size}/{team.limit}", end='\n\n')

def add_to_team(pokemon: Pokemon, team: PokemonTeam) -> bool:
    """Tries to add a new Pokémon to the team, returning whether it actually worked."""
    return team.add_pokemon(pokemon)

def create_pokemon(stats: dict) -> Pokemon:
    """Takes a dictionary of raw stats and turns it into a proper Pokémon object."""
    return Pokemon(
        name=stats["name"],
        id=stats["id"],
        types=stats["types"],
        height=stats["height"],
        weight=stats["weight"],
        base_stats=stats["base_stats"],
    )

def print_shared_weaknesses(team: PokemonTeam) -> None:
    """Figures out if multiple Pokémon on the team share the same type weaknesses and prints them out."""
    weakness_groups = {}

    for pokemon in team.team:
        pokemon_weaknesses = set()

        for pokemon_type in pokemon.types:
            weaknesses = TYPE_WEAKNESSES.get(pokemon_type.lower(), [])
            pokemon_weaknesses.update(weaknesses)

        for weakness in pokemon_weaknesses:
            weakness_groups.setdefault(weakness, []).append(pokemon.name)

    shared = {
        weakness: names
        for weakness, names in weakness_groups.items()
        if len(names) >= 2
    }

    print("Shared weaknesses:\n")

    if not shared:
        print("- No shared weaknesses found.")
        return

    for weakness, names in shared.items():
        formatted_names = format_names(names)

        print(f"- {weakness.title()}")
        print(f"  {formatted_names} are weak to {weakness.title()}.\n")

def format_names(names: list[str]) -> str:
    """Takes a list of names and turns them into a nice, readable sentence with commas and an 'and' at the end."""
    if len(names) == 1:
        return names[0]

    if len(names) == 2:
        return f"{names[0]} and {names[1]}"

    return f"{', '.join(names[:-1])}, and {names[-1]}"

def print_available_types(team: PokemonTeam) -> None:
    """Looks at the whole team and prints out a list of all the different types you currently have."""
    available_types = set()

    for pokemon in team.team:
        available_types.update(pokemon.types)

    print("\nYour available types:\n")

    for pokemon_type in sorted(available_types):
        print(f"- {pokemon_type.title()}")

def print_stats(stats: dict) -> None:
    """Prints out a quick summary of a Pokémon's basic info, like its height and weight."""
    print(f"Name: {stats['name']}")
    print(f"Pokedex ID: {stats['id']}")
    print(f"Type: ")
    print(f"Height: {stats['height']} ft")
    print(f"Weight: {stats['weight']} lbs", end='\n\n')


def print_highest_stats(team: PokemonTeam) -> None:
    """Finds out which Pokémon on the team are the best in specific categories, like the highest HP or fastest speed."""
    categories = {
        "Highest HP": "hp",
        "Highest Attack": "attack",
        "Highest Defense": "defense",
        "Fastest Pokémon": "speed",
    }

    print()

    for label, stat_name in categories.items():
        best_pokemon = max(
            team.team,
            key=lambda pokemon: pokemon.base_stats[stat_name]
        )

        stat_value = best_pokemon.base_stats[stat_name]

        print(f"{label}:")
        print(f"{best_pokemon.name} — {stat_value}\n")
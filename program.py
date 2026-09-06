import sys
import requests
import math

from pokemon import Pokemon
from team import PokemonTeam
from requests.exceptions import HTTPError, ConnectionError, Timeout, JSONDecodeError

POKEMON_LIMIT = 1025
POKEMON_URL = 'https://pokeapi.co/api/v2/pokemon/'


def run_program():
    team = PokemonTeam(limit = 6)

    option_parameters = ['1','2','3','4','5','6']

    print_options()
    option = input("Select an option: ")

    while not option in option_parameters:
        print("Invalid Option. Try again")
        option = input("Select an option: ")

    while True:
        if option == '1':
            run_option_1(team)
        elif option == '2':
            pass
        elif option == '3':
            pass
        elif option == '4':
            pass
        elif option == '5':
            pass
        elif option == '6':
            sys.exit(0)

        print_options()
        option = input("Select an option: ")

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



def search_by_name(pokemon_name: str) -> dict | None:

    pokemon_name = pokemon_name.strip().lower()
    final_url = f"{POKEMON_URL}{pokemon_name}"

    try:

        response = requests.get(final_url, timeout=10) # good practice to set out a timeout

        if response.status_code == 404:
            print(f"Pokemon {pokemon_name} not found")
            return None

        response.raise_for_status()

        data = response.json()

        return data

    except requests.exceptions.Timeout as errt:
        print("Timeout Error: ", errt)
        return None

    except requests.exceptions.HTTPError as err:
        print(f"API request failed: {err}")
        return None



def print_stats(stats: dict) -> None:
    print(f"Name: {stats["name"]}")
    print(f"Pokedex ID: {stats["id"]}")
    print(f"Type: ")
    print(f"Height: {stats["height"]} ft")
    print(f"Weight: {stats["weight"]} lbs")

def get_stats(data: dict) -> dict:
    name = data["name"]
    id = data["id"]
    # types = data["types"]['slot']
    height = round(data["height"] / 3.048, 3)  # decimeter -> feet
    weight = round(data["weight"] / 4.536, 3)  # hectogram -> pound

    return {"name": name , "id": id, "height": height, "weight": weight }

def create_pokemon(stats: dict) -> Pokemon:
    return Pokemon(stats["name"], stats["id"], "blank", stats["height"], stats["weight"])

def add_to_team(pokemon: Pokemon, team) -> PokemonTeam:
    return team.add_pokemon(pokemon)

def search_by_weight():
    pass



def print_options() -> None:
    print("1. Search for a Pokémon",
          "2. Search by weight",
          "3. View team",
          "4. Analyze team",
          "5. Save team",
          "6. Exit", sep='\n')
    print('\n')
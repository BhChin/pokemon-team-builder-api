import sys
import requests
import math

from team import PokemonTeam
from requests.exceptions import HTTPError, ConnectionError, Timeout, JSONDecodeError


# import requests
#
# POKEMON_LIMIT = 1025
# URL = 'https://pokeapi.co/api/v2/pokemon'
# LIMIT_URL = 'https://pokeapi.co/api/v2/pokemon/?limit='
#
# response = requests.get(f"{LIMIT_URL}{POKEMON_LIMIT}&id={35}")
# response2 = requests.get("https://pokeapi.co/api/v2/pokemon/")
#
# data = response2.json()
# print(data)
#
# for pokemon in data['results']:
#     print(pokemon['name'])


def run_program():

    option_parameters = ['1','2','3','4','5','6']

    print_options()

    option = input("Select an option: ")

    while not option in option_parameters:
        print("Invalid Option. Try again")
        option = input("Select an option: ")

    while True:
        if option == '1':
            pokemon = input("Enter a Pokemon Name: ")
            data = search_by_name(pokemon)

            if data is not None:
                print_stats(data)

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

def run_option_1():
    pass

def search_by_name(pokemon_name: str) -> dict | None:
    pokemon_name = pokemon_name.strip().lower()
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    try:

        response = requests.get(pokemon_url, timeout=10) # good practice to set out a timeout

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



def print_stats(data: dict) -> None:
    name = data["name"]
    id = data["id"]
    #types = data["types"]['slot']
    height = round(data["height"]/3.048, 3) # decimeter -> feet
    weight = round(data["weight"]/4.536, 3) # hectogram -> pound

    print(f"Name: {name}")
    print(f"Pokedex ID: {id}")
    print(f"Type: ")
    print(f"Height: {height} ft")
    print(f"Weight: {weight} lbs")


def add_to_team(data: dict, team: PokemonTeam) -> None:
    pass

def search_by_weight():
    pass



def print_options() -> None:
    print("1. Search for a Pokémon",
          "2. Search by weight",
          "3. View team",
          "4. Analyze team",
          "5. Save team",
          "6. Exit", sep='\n')
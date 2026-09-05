import sys

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
        if option == ('1'):
            print("hello")
        elif option == ('2'):
            pass
        elif option == ('3'):
            pass
        elif option == ('4'):
            pass
        elif option == ('5'):
            pass
        elif option == ('6'):
            sys.exit(0)




def print_title() -> None:
    print("================================",
          "      POKÉMON TEAM BUILDER      ",
          "================================", sep='\n')

def print_options() -> None:
    print("1. Search for a Pokémon",
          "2. Search by weight",
          "3. View team",
          "4. Analyze team",
          "5. Save team",
          "6. Exit", sep='\n')
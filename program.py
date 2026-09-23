import sys
from menu_options import *
from database import initialize_database

def run_program():
    initialize_database()

    team = PokemonTeam(limit = 6)

    option_parameters = ['1','2','3','4','5','6']

    print_options()
    option = input("Select an option: ")
    print()

    while not option in option_parameters:
        print("Invalid Option. Try again")
        option = input("Select an option: ")
        print()

    while True:
        if option == '1':
            run_option_1(team)
        elif option == '2':
            run_option_2(team)
        elif option == '3':
            run_option_3(team)
        elif option == '4':
            run_option_4(team)
        elif option == '5':
            team = run_option_5(team)
        elif option == '6':
            sys.exit(0)

        print_options()
        option = input("Select an option: ")
        print()

def print_options() -> None:
    print("1. Search for a Pokémon",
          "2. View team",
          "3. Analyze team",
          "4. Save team",
          "5. Load Team",
          "6. Exit", sep='\n', end='\n\n')

if __name__ == "__main__":
    run_program()
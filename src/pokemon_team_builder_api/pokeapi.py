import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, JSONDecodeError

POKEMON_LIMIT = 1025
POKEMON_URL = 'https://pokeapi.co/api/v2/pokemon/'

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

# def search_by_weight(weight: float):
#     url = f"{POKEMON_URL}?limit={POKEMON_LIMIT}"
#     response = requests.get(url, timeout = 10)
#     data = response.json()
#
#     # reconvert lb to hectogram
#     weight_h = weight*4.536
#
#     for pokemon in data["pokemon"]:
#


def get_stats(data: dict) -> dict:
    types = [
        pokemon_type["type"]["name"]
        for pokemon_type in data["types"]
    ]

    base_stats = {
        stat["stat"]["name"]: stat["base_stat"]
        for stat in data["stats"]
    }

    return {
        "name": data["name"].title(),
        "id": data["id"],
        "types": types,
        "height": data["height"] / 10,  # decimeters to meters
        "weight": data["weight"] / 10,  # hectograms to kilograms
        "base_stats": base_stats,
    }

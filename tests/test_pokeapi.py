import unittest

from pokemon_team_builder_api import pokeapi

class TestPokeAPI(unittest.TestCase):

    def test_search_by_name_returns_dict_for_valid_pokemon(self):
        data = pokeapi.search_by_name("pikachu")
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "pikachu")

    def test_search_by_name_returns_none_for_invalid_pokemon(self):
        data = pokeapi.search_by_name("invalidpokemonname")
        self.assertIsNone(data)

    def test_get_stats_returns_correct_structure(self):
        data = pokeapi.search_by_name("bulbasaur")
        stats = pokeapi.get_stats(data)
        self.assertIn("name", stats)
        self.assertIn("id", stats)
        self.assertIn("types", stats)
        self.assertIn("base_stats", stats)

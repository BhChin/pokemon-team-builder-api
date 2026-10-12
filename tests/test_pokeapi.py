import unittest
from unittest.mock import Mock, patch
# bad practice to call the live api for unittests
# better to mock the requests.get method and return a mock response
import requests

from pokemon_team_builder_api import pokeapi

class TestPokeAPI(unittest.TestCase):

    # bad tests since they call the actual api
    # def test_search_by_name_returns_dict_for_valid_pokemon(self):
    #     data = pokeapi.search_by_name("pikachu")
    #     self.assertIsInstance(data, dict)
    #     self.assertEqual(data["name"], "pikachu")
    #
    # def test_search_by_name_returns_none_for_invalid_pokemon(self):
    #     data = pokeapi.search_by_name("invalidpokemonname")
    #     self.assertIsNone(data)
    #
    # def test_get_stats_returns_correct_structure(self):
    #     data = pokeapi.search_by_name("bulbasaur")
    #     stats = pokeapi.get_stats(data)
    #     self.assertIn("name", stats)
    #     self.assertIn("id", stats)
    #     self.assertIn("types", stats)
    #     self.assertIn("base_stats", stats)

    @patch("pokemon_team_builder_api.pokeapi.requests.get")
    def test_search_by_name_returns_data_and_normalizes_name(self, mock_get):
        expected_data = {"name": "pikachu"}
        response = Mock()
        response.status_code = 200
        response.json.return_value = expected_data
        mock_get.return_value = response

        result = pokeapi.search_by_name("  Pikachu ")

        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with(
            "https://pokeapi.co/api/v2/pokemon/pikachu",
            timeout=10,
        )




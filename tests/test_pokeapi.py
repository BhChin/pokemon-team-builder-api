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

    @patch("pokemon_team_builder_api.pokeapi.requests.get")
    def test_search_by_name_returns_none_for_404(self, mock_get):
        response = Mock()
        response.status_code = 404
        mock_get.return_value = response

        result = pokeapi.search_by_name("missingno")

        self.assertIsNone(result)
        response.raise_for_status.assert_not_called()

    @patch("pokemon_team_builder_api.pokeapi.requests.get")
    def test_search_by_name_returns_none_for_http_error(self, mock_get):
        response = Mock()
        response.status_code = 500
        response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "server error"
        )
        mock_get.return_value = response

        result = pokeapi.search_by_name("pikachu")

        self.assertIsNone(result)

    @patch("pokemon_team_builder_api.pokeapi.requests.get")
    def test_search_by_name_returns_none_for_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("request timed out")

        result = pokeapi.search_by_name("pikachu")

        self.assertIsNone(result)

    def test_get_stats_returns_expected_values_and_conversions(self):
        data = {
            "name": "pikachu",
            "id": 25,
            "types": [
                {"type": {"name": "electric"}},
            ],
            "height": 4,
            "weight": 60,
            "stats": [
                {"stat": {"name": "hp"}, "base_stat": 35},
                {"stat": {"name": "speed"}, "base_stat": 90},
            ],
        }

        result = pokeapi.get_stats(data)

        self.assertEqual(result, {
            "name": "Pikachu",
            "id": 25,
            "types": ["electric"],
            "height": 0.4,
            "weight": 6.0,
            "base_stats": {"hp": 35, "speed": 90},
        })




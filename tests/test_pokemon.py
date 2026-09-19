import unittest

from pokemon import Pokemon
from team import PokemonTeam


class SamplePokemon():
    def __init__(self, name: str):
        self._name = name

class TestPokemonTeam(unittest.TestCase):

    def test_pokemon_team_starts_empty(self):
        team = PokemonTeam()
        self.assertEqual(team.size,0)

    def test_add_pokemon_returns_true(self):
        team = PokemonTeam()
        pokemon = SamplePokemon("Bulbasaur")
        self.assertTrue(team.add_pokemon(pokemon)) #type mismatch. should be fine


    def test_add_pokemon_increases_size(self):
        team = PokemonTeam()
        pokemon = SamplePokemon("Bulbasaur")
        team.add_pokemon(pokemon)
        self.assertEqual(team.size, 1)

    def test_team_has_limits(self):
        pass

    def test_default_limit_is_six(self):
        pass

    def test_pokemon_teams_do_not_share_same_lists(self):
        pass


if __name__ == '__main__':
    unittest.main()


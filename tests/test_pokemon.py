import unittest

from team import PokemonTeam

class TestPokemonTeam(unittest.TestCase):

    def test_pokemon_team_starts_empty(self):
        team = PokemonTeam()
        self.assertEqual(team.size,0)


if __name__ == '__main__':
    unittest.main()


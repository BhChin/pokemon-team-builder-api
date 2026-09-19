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

    def test_team_stores_pokemon(self):
        team = PokemonTeam()
        pokemon = SamplePokemon("Bulbasaur")
        team.add_pokemon(pokemon)

        #self.assertEqual(team.team[0], pokemon)
        #team.team[0] is a bit redundant and stupid
        #to fix we can add a dunder method __getitem__ to allow subscripting
        self.assertEqual(team[0], pokemon)

    def test_add_pokemon_increases_size(self):
        team = PokemonTeam()
        pokemon = SamplePokemon("Bulbasaur")
        team.add_pokemon(pokemon)
        self.assertEqual(team.size, 1)

    def test_team_has_limits(self):
        team = PokemonTeam(limit=2)
        team.add_pokemon(SamplePokemon("Pikachu"))
        team.add_pokemon(SamplePokemon("Bulbasaur"))

        result = team.add_pokemon(SamplePokemon("Charmander"))

        self.assertFalse(result)
        self.assertEqual(team.size, 2)

    def test_default_limit_is_six(self):
        team = PokemonTeam()
        for i in range(6):
            self.assertTrue(team.add_pokemon(SamplePokemon(f"pokemon-{i}")))
        self.assertFalse(team.add_pokemon(SamplePokemon("overlimit")))

    def test_pokemon_teams_do_not_share_same_lists(self):
        team1 = PokemonTeam()
        team2 = PokemonTeam()
        team1.add_pokemon(SamplePokemon("Bulbasaur"))

        self.assertEqual(team1.size, 1)
        self.assertEqual(team2.size, 0)



if __name__ == '__main__':
    unittest.main()


import sqlite3
from team import PokemonTeam

DATABASE = 'pokemon.db'

def initialize_database() -> None:

    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON;")

    connection.execute(
        '''
        CREATE TABLE IF NOT EXISTS pokemon (
            pokemon_id INTEGER PRIMARY KEY
            name TEXT NOT NULL,
            primary_type TEXT NOT NULL,
            secondary_type TEXT,
            height REAL NOT NULL,
            weight REAL NOT NULL,
            hp INTEGER NOT NULL,
            attack INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            special_attack INTEGER NOT NULL,
            special_defense INTEGER NOT NULL,
            speed INTEGER NOT NULL
        ) STRICT;
        '''
    )

    connection.execute(
        '''
        CREATE TABLE IF NOT EXISTS teams(
            team_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
        ) STRICT;
        '''
    )

    connection.execute(
        '''
        CREATE TABLE IF NOT EXISTS team_members
            team_id INTEGER NOT NULL,
            pokemon_id INTEGER NOT NULL,
            position INTEGER NOT NULL,
            
            PRIMARY KEY (team_id, position),
            
            FOREIGN KEY(team_id) REFERENCES teams(team_id),
            
            FOREIGN KEY(pokemon_id) REFERENCES pokemon(pokemon_id)
        ) STRICT;
        '''
    )

    connection.commit()
    connection.close()

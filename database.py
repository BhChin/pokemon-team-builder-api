import sqlite3
from team import PokemonTeam

DATABASE = 'pokemon.db'

def initialize_database() -> None:

    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON;")

    connection.execute(
        '''
        CREATE TABLE IF NOT EXISTS pokemon(
            pokemon_id INTEGER PRIMARY KEY,
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
            name TEXT NOT NULL
        ) STRICT;
        '''
    )

    connection.execute(
        '''
        CREATE TABLE IF NOT EXISTS team_members(
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

def save_team(team_name: str, team: PokemonTeam) -> None:
    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON;")

    team_cursor = connection.execute(
        """
        INSERT INTO teams(name)
        VALUES (?);
        """,
        (team_name,)
    )

    team_id = team_cursor.lastrowid

    for position, pokemon in enumerate(team.team, start=1):
        save_pokemon_if_needed(connection, pokemon)

        connection.execute(
            """
            INSERT INTO team_members(
                team_id,
                pokemon_id,
                position
            )
            VALUES (?, ?, ?);
            """,
            (
                team_id,
                pokemon.id,
                position
            )
        )

    connection.commit()
    connection.close()


def save_pokemon_if_needed(
    connection: sqlite3.Connection,
    pokemon
) -> None:
    cursor = connection.execute(
        """
        SELECT pokemon_id
        FROM pokemon
        WHERE pokemon_id = ?;
        """,
        (pokemon.id,)
    )

    existing_pokemon = cursor.fetchone()

    if existing_pokemon is not None:
        return

    primary_type = pokemon.types[0]
    secondary_type = None

    if len(pokemon.types) == 2:
        secondary_type = pokemon.types[1]

    connection.execute(
        """
        INSERT INTO pokemon(
            pokemon_id,
            name,
            primary_type,
            secondary_type,
            height,
            weight,
            hp,
            attack,
            defense,
            special_attack,
            special_defense,
            speed
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (
            pokemon.id,
            pokemon.name,
            primary_type,
            secondary_type,
            pokemon.height,
            pokemon.weight,
            pokemon.base_stats["hp"],
            pokemon.base_stats["attack"],
            pokemon.base_stats["defense"],
            pokemon.base_stats["special-attack"],
            pokemon.base_stats["special-defense"],
            pokemon.base_stats["speed"]
        )
    )
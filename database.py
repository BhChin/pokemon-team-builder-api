import sqlite3

from pokemon import Pokemon
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


def save_pokemon_if_needed(connection: sqlite3.Connection,pokemon) -> None:
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

def get_team_names() -> list[tuple[int, str]]:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.execute(
        """
        SELECT team_id, name
        FROM teams
        ORDER BY team_id;
        """
    )
    teams = cursor.fetchall()
    connection.close()
    return teams


def load_team(team_id: int) -> PokemonTeam | None:
    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON;")

    cursor = connection.execute(
        """
        SELECT p.pokemon_id, p.name, p.primary_type, p.secondary_type,
               p.height, p.weight, p.hp, p.attack, p.defense,
               p.special_attack, p.special_defense, p.speed
        FROM team_members tm
        JOIN pokemon p ON p.pokemon_id = tm.pokemon_id
        WHERE tm.team_id = ?
        ORDER BY tm.position;
        """,
        (team_id,)
    )
    rows = cursor.fetchall()
    connection.close()

    if not rows:
        return None

    loaded_team = PokemonTeam(limit=6)
    for (pokemon_id, name, primary_type, secondary_type,
         height, weight, hp, attack, defense,
         special_attack, special_defense, speed) in rows:

        types = [primary_type]
        if secondary_type is not None:
            types.append(secondary_type)

        pokemon = Pokemon(
            name=name,
            id=pokemon_id,
            types=types,
            height=height,
            weight=weight,
            base_stats={
                "hp": hp,
                "attack": attack,
                "defense": defense,
                "special-attack": special_attack,
                "special-defense": special_defense,
                "speed": speed,
            },
        )
        loaded_team.add_pokemon(pokemon)

    return loaded_team
import os
import sqlite3
from sqlite3 import Cursor, Connection

from _ask_gpt import chat_with_gpt_3

# Create a new database or connect to an existing one
conn: Connection = sqlite3.connect("dnd5e.db")
cursor: Cursor = conn.cursor()

# Create a table for character information
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Characters (
        id INTEGER PRIMARY KEY,
        name TEXT,
        race TEXT,
        class TEXT,
        level INTEGER
    )
"""
)

# Create a table for monster information
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Monsters (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        challenge_rating REAL
    )
"""
)

# Create a table for item information
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        description TEXT
    )
"""
)

# Create a table for spell information
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Spells (
        id INTEGER PRIMARY KEY,
        name TEXT,
        level INTEGER,
        description TEXT
    )
"""
)

# Create tables for races and classes
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Races (
    id INTEGER PRIMARY KEY,
    name TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS RaceAttributes (
    id INTEGER PRIMARY KEY,
    race_id INTEGER,
    attribute TEXT,
    value TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Classes (
    id INTEGER PRIMARY KEY,
    name TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS ClassAttributes (
    id INTEGER PRIMARY KEY,
    class_id INTEGER,
    attribute TEXT,
    value TEXT
)
"""
)

for file in os.listdir("sql"):
    with open("sql/" + file, "r") as table:
        need_skip = True
        dev_response: str = chat_with_gpt_3(
            question="as a SQL assistant generate SQL insert data for parameters"
            + table.read().split("primary key,")[1]
            + "in the table "
            + file
            + "do not create more than 10 values"
            + "only give SQL code as answer every value should be randomized logical answer for dnd5",
        )
        dev_response_upgraded = "INSERT" + dev_response.split("INSERT")[1].replace("\n", "")
        print(f"dev_response_upgraded {dev_response_upgraded}")
        try:
            cursor.execute(dev_response_upgraded)
        except:
            dev_response_upgraded = f"{dev_response_upgraded}')"
            cursor.execute(dev_response_upgraded)
        conn.commit()

# Commit the changes and close the connection
conn.close()

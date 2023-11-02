import os
import sqlite3

# Connect to the database
connection = sqlite3.connect("dnd5e.db")
cursor = connection.cursor()


# Function to fetch a random row from a table
def get_random_row(table_name: str) -> tuple[str, ...] | None:
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    if row:
        return row
    return None


tables = []
for file in os.listdir("sql"):
    if file.endswith(".sql"):
        tables.append(file.split(".")[0])

# Get random values from each table
for table_name in tables:
    random_row = get_random_row(table_name=table_name)
    if random_row:
        print(f"Random value from {table_name}: {random_row}")
    else:
        print(f"No data found in {table_name}")

# Close the database connection
connection.close()

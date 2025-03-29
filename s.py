# create_database.py
import sqlite3
import csv

def create_tables(cursor):
    # Création des tables (exemple pour Lieu)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Lieu (
            id_lieux INTEGER PRIMARY KEY,
            atmosphere TEXT,
            latitude REAL,
            longitude REAL,
            categorie_route TEXT,
            surface TEXT
        )
    ''')
    # [...] Autres tables

def import_csv(cursor, filename, table):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?']*len(columns))})"
        cursor.executemany(query, (tuple(row.values()) for row in reader))

conn = sqlite3.connect('accidents.db')
cursor = conn.cursor()
create_tables(cursor)
import_csv(cursor, 'lieux.csv', 'Lieu')
# [...] Import des autres fichiers
conn.commit()
conn.close()

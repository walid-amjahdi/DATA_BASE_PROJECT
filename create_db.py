import sqlite3

# Connexion à SQLite
conn = sqlite3.connect("db.sqlite")
cur = conn.cursor()

# Chargement du schéma
with open("init_db.sql", "r") as f:
    cur.executescript(f.read())

# Chargement des données
with open("insert_data.sql", "r") as f:
    cur.executescript(f.read())

# Enregistrement + fermeture
conn.commit()
conn.close()

print("✅ Base db.sqlite créée avec succès avec les données.")

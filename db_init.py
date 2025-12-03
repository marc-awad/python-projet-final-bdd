from db import db, verify_connection, close_connection
from constants import *

if not verify_connection():
    print("Impossible d'initialiser la base de données.")
    exit(1)

print("Connexion MongoDB établie")
print("Initialisation de la base de données...\n")

# Collections pour personnages et monstres
personnages_collection = db[COLLECTION_PERSONNAGES]
monstres_collection = db[COLLECTION_MONSTRES]

# Nettoyage des collections avant insertion
personnages_collection.delete_many({})
monstres_collection.delete_many({})

# Insertion des 10 personnages
personnages = [
    {"nom": "Guerrier", "atk": 15, "defense": 10, "pv": 100},
    {"nom": "Mage", "atk": 20, "defense": 5, "pv": 80},
    {"nom": "Archer", "atk": 18, "defense": 7, "pv": 90},
    {"nom": "Voleur", "atk": 22, "defense": 8, "pv": 85},
    {"nom": "Paladin", "atk": 14, "defense": 12, "pv": 110},
    {"nom": "Sorcier", "atk": 25, "defense": 3, "pv": 70},
    {"nom": "Chevalier", "atk": 17, "defense": 15, "pv": 120},
    {"nom": "Moine", "atk": 19, "defense": 9, "pv": 95},
    {"nom": "Berserker", "atk": 23, "defense": 6, "pv": 105},
    {"nom": "Chasseur", "atk": 16, "defense": 11, "pv": 100},
]

# Insertion des 10 monstres
monstres = [
    {"nom": "Gobelin", "atk": 10, "defense": 5, "pv": 50},
    {"nom": "Orc", "atk": 20, "defense": 8, "pv": 120},
    {"nom": "Dragon", "atk": 35, "defense": 20, "pv": 300},
    {"nom": "Zombie", "atk": 12, "defense": 6, "pv": 70},
    {"nom": "Troll", "atk": 25, "defense": 15, "pv": 200},
    {"nom": "Spectre", "atk": 18, "defense": 10, "pv": 100},
    {"nom": "Golem", "atk": 30, "defense": 25, "pv": 250},
    {"nom": "Vampire", "atk": 22, "defense": 12, "pv": 150},
    {"nom": "Loup-garou", "atk": 28, "defense": 18, "pv": 180},
    {"nom": "Squelette", "atk": 15, "defense": 7, "pv": 90},
]

# Insertion en base de données
personnages_collection.insert_many(personnages)
monstres_collection.insert_many(monstres)

# Nettoyage de la collection des scores
scores_collection = db[COLLECTION_SCORES]
scores_collection.delete_many({})
from pymongo import MongoClient

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["jeu_video"]

# Collections pour personnages et monstres
personnages_collection = db["personnages"]
monstres_collection = db["monstres"]

# Nettoyage des collections avant insertion
personnages_collection.delete_many({})
monstres_collection.delete_many({})

# Insertion des 10 personnages
personnages = [
    {"nom": "Guerrier", "atk": 15, "def": 10, "pv": 100},
    {"nom": "Mage", "atk": 20, "def": 5, "pv": 80},
    {"nom": "Archer", "atk": 18, "def": 7, "pv": 90},
    {"nom": "Voleur", "atk": 22, "def": 8, "pv": 85},
    {"nom": "Paladin", "atk": 14, "def": 12, "pv": 110},
    {"nom": "Sorcier", "atk": 25, "def": 3, "pv": 70},
    {"nom": "Chevalier", "atk": 17, "def": 15, "pv": 120},
    {"nom": "Moine", "atk": 19, "def": 9, "pv": 95},
    {"nom": "Berserker", "atk": 23, "def": 6, "pv": 105},
    {"nom": "Chasseur", "atk": 16, "def": 11, "pv": 100},
]

# Insertion des 10 monstres
monstres = [
    {"nom": "Gobelin", "atk": 10, "def": 5, "pv": 50},
    {"nom": "Orc", "atk": 20, "def": 8, "pv": 120},
    {"nom": "Dragon", "atk": 35, "def": 20, "pv": 300},
    {"nom": "Zombie", "atk": 12, "def": 6, "pv": 70},
    {"nom": "Troll", "atk": 25, "def": 15, "pv": 200},
    {"nom": "Spectre", "atk": 18, "def": 10, "pv": 100},
    {"nom": "Golem", "atk": 30, "def": 25, "pv": 250},
    {"nom": "Vampire", "atk": 22, "def": 12, "pv": 150},
    {"nom": "Loup-garou", "atk": 28, "def": 18, "pv": 180},
    {"nom": "Squelette", "atk": 15, "def": 7, "pv": 90},
]

# Insertion en base de données
personnages_collection.insert_many(personnages)
monstres_collection.insert_many(monstres)

# Nettoyage de la collection des scores
scores_collection = db["scores"]
scores_collection.delete_many({})  
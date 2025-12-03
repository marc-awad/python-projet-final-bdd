from db import db, verify_connection, close_connection
from constants import *


def initialiser_base_donnees():
    """Initialise la base de données avec des personnages et monstres par défaut"""
    if not verify_connection():
        print("Impossible d'initialiser la base de données.")
        exit(1)

    print("Connexion MongoDB établie")
    print("Initialisation de la base de données...\n")

    _nettoyer_collections()
    _inserer_personnages()
    _inserer_monstres()
    _nettoyer_scores()
    
    print("Base de données initialisée avec succès !")
    close_connection()


def _nettoyer_collections():
    """Supprime toutes les données existantes des collections"""
    db[COLLECTION_PERSONNAGES].delete_many({})
    db[COLLECTION_MONSTRES].delete_many({})
    print("Collections nettoyées.")


def _nettoyer_scores():
    """Supprime tous les scores existants"""
    db[COLLECTION_SCORES].delete_many({})
    print("Scores réinitialisés.")


def _inserer_personnages():
    """Insère les personnages jouables dans la base de données"""
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
    
    db[COLLECTION_PERSONNAGES].insert_many(personnages)
    print(f"{len(personnages)} personnages insérés.")


def _inserer_monstres():
    """Insère les monstres dans la base de données"""
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
    
    db[COLLECTION_MONSTRES].insert_many(monstres)
    print(f"{len(monstres)} monstres insérés.")


if __name__ == "__main__":
    initialiser_base_donnees()
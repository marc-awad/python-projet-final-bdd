from db import get_db, verify_connection, close_connection
from constants import *


def initialiser_base_donnees():
    """Initialise la base de données avec des personnages et monstres par défaut"""
    if not verify_connection():
        exit(1)

    _afficher_debut_initialisation()
    _executer_initialisation()
    _afficher_fin_initialisation()

    close_connection()



def _afficher_debut_initialisation():
    """Affiche les messages de début d'initialisation"""
    print("Connexion MongoDB établie")
    print("Initialisation de la base de données...\n")


def _afficher_fin_initialisation():
    """Affiche le message de fin d'initialisation"""
    print("Base de données initialisée avec succès !")


def _executer_initialisation():
    """Exécute toutes les étapes d'initialisation"""
    _nettoyer_collections()
    _peupler_collections()
    _nettoyer_scores()


def _nettoyer_collections():
    """Supprime toutes les données existantes des collections"""
    _vider_collection(COLLECTION_PERSONNAGES)
    _vider_collection(COLLECTION_MONSTRES)
    print("Collections nettoyées.")


def _vider_collection(nom_collection):
    """Vide une collection spécifique"""
    get_db()[nom_collection].delete_many({})


def _peupler_collections():
    """Peuple les collections avec les données par défaut"""
    _inserer_personnages()
    _inserer_monstres()


def _nettoyer_scores():
    """Supprime tous les scores existants"""
    _vider_collection(COLLECTION_SCORES)
    print("Scores réinitialisés.")


def _inserer_personnages():
    """Insère les personnages jouables dans la base de données"""
    personnages = _creer_donnees_personnages()
    _inserer_entites(COLLECTION_PERSONNAGES, personnages, "personnages")


def _inserer_monstres():
    """Insère les monstres dans la base de données"""
    monstres = _creer_donnees_monstres()
    _inserer_entites(COLLECTION_MONSTRES, monstres, "monstres")


def _inserer_entites(collection, entites, nom_type):
    """Insère des entités dans une collection"""
    get_db()[collection].insert_many(entites)
    print(f"{len(entites)} {nom_type} insérés.")


def _creer_donnees_personnages():
    """Crée la liste des personnages par défaut"""
    return [
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


def _creer_donnees_monstres():
    """Crée la liste des monstres par défaut"""
    return [
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


if __name__ == "__main__":
    initialiser_base_donnees()

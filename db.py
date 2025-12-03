from pymongo import MongoClient
from constants import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def verify_connection():
    """Vérifie que la connexion MongoDB est opérationnelle"""
    try:
        client.admin.command('ping')
        return True
    except Exception as e:
        print(f"Erreur de connexion MongoDB : {e}")
        print("Veuillez démarrer MongoDB et relancer le jeu.")
        return False


def close_connection():
    """Ferme proprement la connexion à MongoDB"""
    client.close()
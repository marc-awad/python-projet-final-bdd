from pymongo import MongoClient
from constants import MONGO_URI, DB_NAME

# Variables privées pour lazy loading
_client = None
_db = None


def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(MONGO_URI)
        _db = _client[DB_NAME]
    return _db


def verify_connection():
    try:
        get_db().client.admin.command('ping')
        return True
    except Exception as e:
        print(f"Erreur de connexion MongoDB : {e}")
        print("Veuillez démarrer MongoDB et relancer le jeu.")
        return False


def close_connection():
    """Ferme proprement la connexion à MongoDB"""
    global _client
    if _client is not None:
        _client.close()
        _client = None
        _db = None
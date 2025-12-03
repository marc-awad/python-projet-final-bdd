from pymongo import MongoClient
from constants import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def verify_connection():
    try:
        client.admin.command('ping')
        return True
    except Exception as e:
        print(f"Erreur de connexion MongoDB : {e}")
        print("Veuillez démarrer MongoDB et relancer le jeu.")
        return False

def close_connection():
    client.close()
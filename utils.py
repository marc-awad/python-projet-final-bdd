from pymongo import MongoClient
import random
from constants import *
from models import Personnage, Monstre
import os

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_all_personnages():
    try:
        personnages_data = list(db[COLLECTION_PERSONNAGES].find())
        if not personnages_data:
            print("Attention : Aucun personnage trouvé dans la base de données.")
            return []
        personnages = [
            Personnage(p['nom'], p['atk'], p['defense'], p['pv']) 
            for p in personnages_data
        ]
        return personnages
    except Exception as e:
        print(f"Erreur lors de la récupération des personnages : {e}")
        print("Veuillez vérifier que MongoDB est démarré et accessible.")
        return []

def get_random_monstre():
    try:
        monstres_data = list(db[COLLECTION_MONSTRES].find())
        if not monstres_data:
            print("Attention : Aucun monstre trouvé dans la base de données.")
            return None
        monstre_data = random.choice(monstres_data)
        monstre = Monstre(
            monstre_data['nom'], 
            monstre_data['atk'], 
            monstre_data['defense'], 
            monstre_data['pv']
        )
        return monstre
    except Exception as e:
        print(f"Erreur lors de la récupération des monstres : {e}")
        print("Veuillez vérifier que MongoDB est démarré et accessible.")
        return None

def get_top_scores(limit=TOP_SCORES_LIMIT):
    try:
        scores = db[COLLECTION_SCORES].find().sort("vagues", -1).limit(limit)
        scores_list = list(scores)
        if not scores_list:
            return []
        return scores_list
    except Exception as e:
        print(f"Erreur lors de la récupération des scores : {e}")
        print("Veuillez vérifier que MongoDB est démarré et accessible.")
        return []

def afficher_pv(equipe, monstre):
    for p in equipe:
        print(f"{p.nom} - PV: {p.pv}/{p.pv_max}")
    print(f"{monstre.nom} - PV: {monstre.pv}/{monstre.pv_max}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
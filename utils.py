from pymongo import MongoClient
import random
from constants import *

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_all_personnages():
    return list(db[COLLECTION_PERSONNAGES].find())

def get_random_monstre():
    monstres = list(db[COLLECTION_MONSTRES].find())
    return random.choice(monstres) if monstres else None

def get_top_scores(limit=TOP_SCORES_LIMIT):
    scores = db[COLLECTION_SCORES].find().sort("vagues", -1).limit(limit)
    return list(scores)

def calculer_degats(atk, defense):
    return max(atk - defense, 0)


def afficher_pv(equipe_pv, equipe, monstre_pv, monstre_nom):
    for i, p in enumerate(equipe):
        print(f"{p['nom']} - PV: {equipe_pv[i]}")
    print(f"{monstre_nom} - PV: {monstre_pv}")

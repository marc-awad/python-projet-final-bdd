from pymongo import MongoClient
import random

client = MongoClient("mongodb://localhost:27017")
db = client["jeu_video"]

def get_all_personnages():
    return list(db["personnages"].find())

def get_random_monstre():
    monstres = list(db["monstres"].find())
    return random.choice(monstres) if monstres else None

def get_top_scores(limit=3):
    scores = db["scores"].find().sort("vagues", -1).limit(limit)
    return list(scores)

def calculer_degats(atk, defense):
    return max(atk - defense, 0)


def afficher_pv(equipe_pv, equipe, monstre_pv, monstre_nom):
    for i, p in enumerate(equipe):
        print(f"{p['nom']} - PV: {equipe_pv[i]}")
    print(f"{monstre_nom} - PV: {monstre_pv}")

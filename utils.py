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

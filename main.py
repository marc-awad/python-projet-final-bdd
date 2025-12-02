from pymongo import MongoClient
from models import Personnage, Monstre

client = MongoClient("mongodb://localhost:27017")
db = client["jeu_video"]

# Test d'insertion et d'affichage
p = Personnage("Guerrier", 15, 10, 100)
m = Monstre("Gobelin", 10, 5, 50)

print(p)
print(m)

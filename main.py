from pymongo import MongoClient
from models import Personnage, Monstre
from utils import get_all_personnages, get_random_monstre

client = MongoClient("mongodb://localhost:27017")
db = client["jeu_video"]

# Test d'insertion et d'affichage
p = Personnage("Guerrier", 15, 10, 100)
m = Monstre("Gobelin", 10, 5, 50)

print(p)
print(m)

# Tester la récupération de tous les personnages
for p in get_all_personnages():
    print(p)


# Tester la récupération d'un monstre aléatoire
print(get_random_monstre())

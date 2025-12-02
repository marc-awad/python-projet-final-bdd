from pymongo import MongoClient
from models import Personnage, Monstre
from utils import get_all_personnages, get_random_monstre, get_top_scores

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


#Test des scores
db["scores"].insert_one({"joueur": "Marc", "vagues": 5})
print("Top scores :", get_top_scores())

from utils import get_top_scores

while True:
    print("\n=== MENU PRINCIPAL ===")
    print("1. Démarrer le jeu")
    print("2. Classement")
    print("3. Quitter")

    choix = input("Choisissez une option : ")

    if choix == "1":
        print("Démarrage du jeu...")
    elif choix == "2":
        scores = get_top_scores()
        if scores:
            for i, s in enumerate(scores, 1):
                print(f"{i}. {s['joueur']} - Vagues : {s['vagues']}")
        else:
            print("Aucun score disponible.")
    elif choix == "3":
        print("Au revoir !")
        break
    else:
        print("Option invalide.")


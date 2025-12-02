import random
import time
from utils import get_random_monstre, get_all_personnages, get_top_scores
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["jeu_video"]

def afficher_classement():
    try:
        scores = get_top_scores(3)
        if not scores:
            print("Aucun score disponible.")
            return

        print("\n=== TOP 3 DES SCORES ===")
        print(f"{'Rang':<5}{'Joueur':<15}{'Vagues':<7}")
        print("-" * 27)
        for rang, score in enumerate(scores, start=1):
            print(f"{rang:<5}{score['joueur']:<15}{score['vagues']:<7}")
    except Exception as e:
        print(f"Erreur lors de l'affichage du classement : {e}")

def combat_par_vagues(equipe, nom_joueur):
    vague = 1
    while True:
        try:
            monstre = get_random_monstre()
            if not monstre:
                print("Aucun monstre disponible.")
                break

            monstre_pv = monstre['pv']
            equipe_pv = [p['pv'] for p in equipe]

            print(f"\n=== Vague {vague} ===")
            print(f"Monstre rencontré : {monstre['nom']} - ATK: {monstre['atk']}, DEF: {monstre['defense']}, PV: {monstre_pv}")

            while monstre_pv > 0 and any(pv > 0 for pv in equipe_pv):
                for i, p in enumerate(equipe):
                    if equipe_pv[i] <= 0:
                        continue
                    print(f"{p['nom']} attaque {monstre['nom']}", end="", flush=True)
                    for _ in range(3):
                        time.sleep(0.6)
                        print(" .", end="", flush=True)
                    degats = max(p['atk'] - monstre['defense'], 0)
                    monstre_pv -= degats
                    print(f" => {degats} dégâts (PV monstre: {max(monstre_pv,0)})")
                    if monstre_pv <= 0:
                        break

                if monstre_pv <= 0:
                    print(f"{monstre['nom']} est vaincu !")
                    break

                indices_vivants = [i for i, pv in enumerate(equipe_pv) if pv > 0]
                cible_idx = random.choice(indices_vivants)
                print(f"{monstre['nom']} attaque {equipe[cible_idx]['nom']}", end="", flush=True)
                for _ in range(3):
                    time.sleep(0.3)
                    print(" .", end="", flush=True)
                degats = max(monstre['atk'] - equipe[cible_idx]['defense'], 0)
                equipe_pv[cible_idx] -= degats
                print(f" => {degats} dégâts (PV restant: {max(equipe_pv[cible_idx],0)})")

            if all(pv <= 0 for pv in equipe_pv):
                print("\nTous vos personnages sont morts. Défaite !")
                db["scores"].insert_one({"joueur": nom_joueur, "vagues": vague-1})
                print(f"Votre score de {vague-1} vagues a été enregistré !")
                break

            vague += 1
            print(f"Vague {vague-1} terminée !")
        except Exception as e:
            print(f"Erreur pendant le combat : {e}")
            break


while True:
    try:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Démarrer le jeu")
        print("2. Classement")
        print("3. Quitter")

        choix = input("Choisissez une option : ").strip()

        if choix == "1":
            nom_joueur = ""
            while not nom_joueur:
                nom_joueur = input("Entrez votre nom : ").strip()
                if not nom_joueur:
                    print("Nom invalide. Réessayez.")

            print(f"Bienvenue {nom_joueur}, vous allez maintenant créer votre équipe de 3 personnages.")

            personnages = get_all_personnages()
            if not personnages:
                print("Aucun personnage disponible. Retour au menu.")
                continue

            print("\nListe des personnages disponibles :")
            for idx, p in enumerate(personnages, 1):
                print(f"{idx}. {p['nom']} - ATK: {p['atk']}, DEF: {p['defense']}, PV: {p['pv']}")

            equipe = []
            while len(equipe) < 3:
                choix_perso = input(f"Sélectionnez le personnage #{len(equipe)+1} (1-{len(personnages)}): ").strip()
                if not choix_perso.isdigit() or int(choix_perso) < 1 or int(choix_perso) > len(personnages):
                    print("Choix invalide, réessayez.")
                    continue
                perso = personnages[int(choix_perso)-1]
                if perso in equipe:
                    print("Personnage déjà choisi, choisissez un autre.")
                    continue
                equipe.append(perso)

            print("\nVotre équipe :")
            for p in equipe:
                print(f"{p['nom']} - ATK: {p['atk']}, DEF: {p['defense']}, PV: {p['pv']}")

            combat_par_vagues(equipe, nom_joueur)

        elif choix == "2":
            afficher_classement()
        elif choix == "3":
            print("Au revoir !")
            break
        else:
            print("Option invalide, réessayez.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

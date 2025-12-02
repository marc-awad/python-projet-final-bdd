# main.py
import random
import time
from utils import get_random_monstre, get_all_personnages, get_top_scores, calculer_degats, afficher_pv
from constants import *

from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def afficher_classement():
    try:
        scores = get_top_scores(TOP_SCORES_LIMIT)
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
        monstre = get_random_monstre()
        if not monstre:
            print(MSG_AUCUN_MONSTRE)
            break

        monstre_pv = monstre['pv']
        equipe_pv = [p['pv'] for p in equipe]

        print(f"\n=== Vague {vague} ===")
        print(f"Monstre rencontré : {monstre['nom']} - ATK: {monstre['atk']}, DEF: {monstre['defense']}, PV: {monstre_pv}")

        while monstre_pv > 0 and any(pv > 0 for pv in equipe_pv):
            for i, p in enumerate(equipe):
                if equipe_pv[i] <= 0:
                    continue
                degats = calculer_degats(p['atk'], monstre['defense'])
                monstre_pv -= degats
                print(f"{p['nom']} attaque {monstre['nom']} => {degats} dégâts (PV monstre: {max(monstre_pv,0)})")
                time.sleep(DELAY_ATTAQUE_PERSONNAGE)
                if monstre_pv <= 0:
                    break

            if monstre_pv <= 0:
                print(f"{monstre['nom']}{MSG_VICTOIRE}")
                break

            indices_vivants = [i for i, pv in enumerate(equipe_pv) if pv > 0]
            cible_idx = random.choice(indices_vivants)
            degats = calculer_degats(monstre['atk'], equipe[cible_idx]['defense'])
            equipe_pv[cible_idx] -= degats
            print(f"{monstre['nom']} attaque {equipe[cible_idx]['nom']} => {degats} dégâts (PV restant: {max(equipe_pv[cible_idx],0)})")
            time.sleep(DELAY_ATTAQUE_MONSTRE)
            afficher_pv(equipe_pv, equipe, monstre_pv, monstre['nom'])

        if all(pv <= 0 for pv in equipe_pv):
            print(f"\n{MSG_DEFAITE}")
            db[COLLECTION_SCORES].insert_one({"joueur": nom_joueur, "vagues": vague-1})
            print(f"Votre score de {vague-1} vagues a été enregistré !")
            break

        vague += 1
        print(f"Vague {vague-1} terminée !")



def saisie_joueur():
    nom = ""
    while not nom:
        nom = input("Entrez votre nom : ").strip()
        if not nom:
            print("Nom invalide. Réessayez.")
    return nom

def selection_equipe(personnages):
    equipe = []
    while len(equipe) < NB_PERSONNAGES_EQUIPE:
        choix_perso = input(f"Sélectionnez le personnage #{len(equipe)+1} (1-{len(personnages)}): ").strip()
        if not choix_perso.isdigit() or int(choix_perso) < 1 or int(choix_perso) > len(personnages):
            print("Choix invalide, réessayez.")
            continue
        perso = personnages[int(choix_perso)-1]
        if perso in equipe:
            print("Personnage déjà choisi, choisissez un autre.")
            continue
        equipe.append(perso)
    return equipe

def afficher_personnages(personnages):
    print("\nListe des personnages disponibles :")
    for idx, p in enumerate(personnages, 1):
        print(f"{idx}. {p['nom']} - ATK: {p['atk']}, DEF: {p['defense']}, PV: {p['pv']}")

def initialize_game():
    print("Bienvenue dans le jeu de combat par vagues !")
    nom_joueur = saisie_joueur()
    personnages = get_all_personnages()
    if not personnages:
        print("Aucun personnage disponible. Retour au menu.")
    afficher_personnages(personnages)
    equipe = selection_equipe(personnages)
    print("\nVotre équipe :")
    for p in equipe:
        print(f"{p['nom']} - ATK: {p['atk']}, DEF: {p['defense']}, PV: {p['pv']}")
    combat_par_vagues(equipe, nom_joueur)

def print_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Démarrer le jeu")
    print("2. Classement")
    print("3. Quitter")

def menu_principal():
    while True:
        try:
            print_menu()

            choix = input("Choisissez une option : ").strip()

            if choix == "1":
                initialize_game()
            elif choix == "2":
                afficher_classement()
            elif choix == "3":
                print("Au revoir !")
                break
            else:
                print("Option invalide, réessayez.")
        except Exception as e:
            print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    menu_principal()

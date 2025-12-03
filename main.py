import random
import time
from utils import get_random_monstre, get_all_personnages, get_top_scores, afficher_pv, clear_screen
from constants import *

from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def afficher_classement():
    try:
        clear_screen()
        scores = get_top_scores(TOP_SCORES_LIMIT)
        if not scores:
            print("Aucun score disponible.")
            return

        print("\n=== TOP 3 DES SCORES ===")
        print(f"{'Rang':<5}{'Joueur':<15}{'Vagues':<7}")
        print("-" * 27)

        for rang, score in enumerate(scores, start=1):
            print(f"{rang:<5}{score['joueur']:<15}{score['vagues']:<7}")

        input("\nAppuyez sur Entrée pour revenir au menu...")
        clear_screen()
    except Exception as e:
        print(f"Erreur lors de l'affichage du classement : {e}")

def combat_par_vagues(equipe, nom_joueur):
    vague = 1
    while True:
        clear_screen()
        monstre = get_random_monstre()
        if not monstre:
            print(MSG_AUCUN_MONSTRE)
            break

        print(f"\n=== Vague {vague} ===")
        print(f"Monstre rencontré : {monstre.nom} - ATK: {monstre.atk}, DEF: {monstre.defense}, PV: {monstre.pv}")

        while monstre.est_vivant() and any(p.est_vivant() for p in equipe):
            for p in equipe:
                if not p.est_vivant():
                    continue
                
                degats = p.attaquer(monstre)
                print(f"{p.nom} attaque {monstre.nom} => {degats} dégâts (PV monstre: {monstre.pv})")
                time.sleep(DELAY_ATTAQUE_PERSONNAGE)
                
                if not monstre.est_vivant():
                    break

            if not monstre.est_vivant():
                print(f"{monstre.nom}{MSG_VICTOIRE}")
                break

            personnages_vivants = [p for p in equipe if p.est_vivant()]
            cible = random.choice(personnages_vivants)
            degats = monstre.attaquer(cible)
            print(f"{monstre.nom} attaque {cible.nom} => {degats} dégâts (PV restant: {cible.pv})")
            time.sleep(DELAY_ATTAQUE_MONSTRE)
            afficher_pv(equipe, monstre)

        if not any(p.est_vivant() for p in equipe):
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
        print(f"{idx}. {p.nom} - ATK: {p.atk}, DEF: {p.defense}, PV: {p.pv}")

def initialize_game():
    clear_screen()
    print("Bienvenue dans le jeu de combat par vagues !")
    nom_joueur = saisie_joueur()

    clear_screen()
    personnages = get_all_personnages()
    if not personnages:
        print("Aucun personnage disponible. Retour au menu.")
        return

    afficher_personnages(personnages)
    equipe = selection_equipe(personnages)

    clear_screen()
    print("\nVotre équipe :")
    for p in equipe:
        print(f"{p.nom} - ATK: {p.atk}, DEF: {p.defense}, PV: {p.pv}")

    input("\nAppuyez sur Entrée pour commencer le combat...")
    clear_screen()
    combat_par_vagues(equipe, nom_joueur)


def print_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1. Démarrer le jeu")
    print("2. Classement")
    print("3. Quitter")

def menu_principal():
    try:
        while True:
            clear_screen()
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
    finally:
            client.close()

if __name__ == "__main__":
    menu_principal()
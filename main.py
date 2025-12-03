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
            input("\nAppuyez sur Entrée pour revenir au menu...")
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
        input("\nAppuyez sur Entrée pour revenir au menu...")

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
        nom = input("Entrez votre nom (0 pour annuler) : ").strip()
        if nom == "0":
            return None
        if not nom:
            print("Nom invalide. Réessayez.")
    return nom

def afficher_equipe_en_construction(equipe):
    print("\n=== ÉQUIPE EN COURS DE CONSTRUCTION ===")
    for i in range(NB_PERSONNAGES_EQUIPE):
        if i < len(equipe):
            p = equipe[i]
            print(f"Personnage #{i+1} : {p.nom} - ATK: {p.atk}, DEF: {p.defense}, PV: {p.pv}")
        else:
            print(f"Personnage #{i+1} : [vide]")
    print()

def selection_equipe(personnages):
    equipe = []
    while len(equipe) < NB_PERSONNAGES_EQUIPE:
        clear_screen()
        afficher_equipe_en_construction(equipe)
        afficher_personnages(personnages)
        
        choix_perso = input(f"\nSélectionnez le personnage #{len(equipe)+1} (1-{len(personnages)}, 0 pour annuler) : ").strip()
        
        if not choix_perso.isdigit():
            print("Entrée invalide. Veuillez entrer un nombre.")
            time.sleep(1)
            continue
        
        choix_num = int(choix_perso)
        
        if choix_num == 0:
            print("Sélection annulée. Retour au menu.")
            time.sleep(1)
            return None
        
        if choix_num < 1 or choix_num > len(personnages):
            print(f"Choix invalide. Veuillez choisir entre 1 et {len(personnages)}.")
            time.sleep(1)
            continue
        
        perso = personnages[choix_num - 1]
        if perso in equipe:
            print("Personnage déjà choisi, choisissez un autre.")
            time.sleep(1)
            continue
        
        equipe.append(perso)
        print(f"\n✓ {perso.nom} ajouté à l'équipe !")
        time.sleep(1)
    
    return equipe

def afficher_personnages(personnages):
    print("--- Personnages disponibles ---")
    for idx, p in enumerate(personnages, 1):
        print(f"{idx}. {p.nom} - ATK: {p.atk}, DEF: {p.defense}, PV: {p.pv}")

def initialize_game():
    clear_screen()
    print("Bienvenue dans le jeu de combat par vagues !")
    nom_joueur = saisie_joueur()
    
    if nom_joueur is None:
        print("Retour au menu principal.")
        time.sleep(1)
        return

    clear_screen()
    personnages = get_all_personnages()
    if not personnages:
        print("Aucun personnage disponible. Retour au menu.")
        input("\nAppuyez sur Entrée pour continuer...")
        return

    equipe = selection_equipe(personnages)
    
    if equipe is None:
        return

    clear_screen()
    print("\n=== VOTRE ÉQUIPE FINALE ===")
    for i, p in enumerate(equipe, 1):
        print(f"Personnage #{i} : {p.nom} - ATK: {p.atk}, DEF: {p.defense}, PV: {p.pv}")

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

            choix = input("\nChoisissez une option : ").strip()

            if not choix.isdigit():
                print("Entrée invalide. Veuillez entrer un nombre.")
                time.sleep(1)
                continue

            choix_num = int(choix)

            if choix_num == 1:
                initialize_game()
            elif choix_num == 2:
                afficher_classement()
            elif choix_num == 3:
                print("Au revoir !")
                break
            else:
                print("Option invalide. Veuillez choisir entre 1 et 3.")
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nInterruption détectée. Au revoir !")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        client.close()

if __name__ == "__main__":
    menu_principal()
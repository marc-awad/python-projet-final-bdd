import random
import time
from utils import get_random_monstre, afficher_pv, clear_screen
from constants import *

from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


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


def initialize_game():
    from utils import get_all_personnages
    
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
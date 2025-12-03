import random
import time
from utils import (
    get_random_monstre, 
    afficher_pv, 
    clear_screen, 
    get_top_scores,
    sauvegarder_score,
    afficher_classement_formate,
    saisir_entier,
    attendre_entree,
    get_all_personnages
)
from constants import *


def initialize_game():
    """Point d'entrée du jeu : initialise une nouvelle partie"""
    clear_screen()
    print("Bienvenue dans le jeu de combat par vagues !")
    
    nom_joueur = _saisir_nom_joueur()
    if nom_joueur is None:
        print("Retour au menu principal.")
        time.sleep(DELAY_MESSAGE_COURT)
        return

    personnages_disponibles = get_all_personnages()
    if not personnages_disponibles:
        print(MSG_AUCUN_PERSONNAGE)
        attendre_entree()
        return

    equipe_joueur = _selectionner_equipe(personnages_disponibles)
    if equipe_joueur is None:
        return

    _afficher_equipe_finale(equipe_joueur)
    attendre_entree("\nAppuyez sur Entrée pour commencer le combat...")
    
    clear_screen()
    _lancer_combat_par_vagues(equipe_joueur, nom_joueur)


def _lancer_combat_par_vagues(equipe, nom_joueur):
    """Gère la boucle principale du combat par vagues"""
    numero_vague = 1
    
    while True:
        clear_screen()
        monstre_actuel = get_random_monstre()
        
        if not monstre_actuel:
            print(MSG_AUCUN_MONSTRE)
            break

        _afficher_entete_vague(numero_vague, monstre_actuel)
        
        # Combat jusqu'à la victoire ou la défaite
        if _executer_combat(equipe, monstre_actuel):
            # Victoire : le monstre est vaincu
            print(f"{monstre_actuel.nom}{MSG_VICTOIRE}")
            numero_vague += 1
            print(f"Vague {numero_vague - 1} terminée !")
        else:
            # Défaite : l'équipe est vaincue
            _gerer_defaite(nom_joueur, numero_vague - 1)
            break


def _executer_combat(equipe, monstre):
    """
    Exécute un combat entre l'équipe et le monstre
    Retourne True si l'équipe gagne, False si elle perd
    """
    while monstre.est_vivant() and _equipe_a_survivants(equipe):
        # Tour des personnages
        for personnage in equipe:
            if not personnage.est_vivant():
                continue
            
            degats_infliges = personnage.attaquer(monstre)
            print(f"{personnage.nom} attaque {monstre.nom} => {degats_infliges} dégâts (PV monstre: {monstre.pv})")
            time.sleep(DELAY_ATTAQUE_PERSONNAGE)
            
            if not monstre.est_vivant():
                return True  # Victoire

        # Tour du monstre (si toujours vivant)
        if monstre.est_vivant():
            _tour_monstre(equipe, monstre)
            afficher_pv(equipe, monstre)

    return False  # Défaite


def _tour_monstre(equipe, monstre):
    """Le monstre attaque un personnage vivant au hasard"""
    cibles_vivantes = [p for p in equipe if p.est_vivant()]
    cible = random.choice(cibles_vivantes)
    
    degats_infliges = monstre.attaquer(cible)
    print(f"{monstre.nom} attaque {cible.nom} => {degats_infliges} dégâts (PV restant: {cible.pv})")
    time.sleep(DELAY_ATTAQUE_MONSTRE)


def _gerer_defaite(nom_joueur, vagues_completees):
    """Gère la défaite : sauvegarde le score et affiche le classement"""
    print(f"\n{MSG_DEFAITE}")
    sauvegarder_score(nom_joueur, vagues_completees)
    
    attendre_entree("\nAppuyez sur Entrée pour voir le classement...")
    clear_screen()
    
    scores = get_top_scores(TOP_SCORES_LIMIT)
    afficher_classement_formate(scores)
    attendre_entree()


def _selectionner_equipe(personnages_disponibles):
    """Permet au joueur de sélectionner son équipe de personnages"""
    equipe = []
    
    while len(equipe) < NB_PERSONNAGES_EQUIPE:
        clear_screen()
        _afficher_equipe_en_construction(equipe)
        _afficher_personnages_disponibles(personnages_disponibles)
        
        numero_personnage = len(equipe) + 1
        choix = saisir_entier(
            f"\nSélectionnez le personnage #{numero_personnage} (1-{len(personnages_disponibles)}, 0 pour annuler) : ",
            valeur_min=MENU_ANNULER,
            valeur_max=len(personnages_disponibles)
        )
        
        if choix == MENU_ANNULER:
            print("Sélection annulée. Retour au menu.")
            time.sleep(DELAY_MESSAGE_COURT)
            return None
        
        personnage_choisi = personnages_disponibles[choix - 1]
        
        if personnage_choisi in equipe:
            print("Personnage déjà choisi, choisissez un autre.")
            time.sleep(DELAY_MESSAGE_COURT)
            continue
        
        equipe.append(personnage_choisi)
        print(f"\n✓ {personnage_choisi.nom} ajouté à l'équipe !")
        time.sleep(DELAY_MESSAGE_COURT)
    
    return equipe


def _saisir_nom_joueur():
    """Demande au joueur de saisir son nom"""
    while True:
        nom = input("Entrez votre nom (0 pour annuler) : ").strip()
        
        if nom == "0":
            return None
        
        if nom:
            return nom
        
        print("Nom invalide. Réessayez.")


def _afficher_equipe_en_construction(equipe):
    """Affiche l'équipe en cours de construction"""
    print("\n=== ÉQUIPE EN COURS DE CONSTRUCTION ===")
    for index in range(NB_PERSONNAGES_EQUIPE):
        if index < len(equipe):
            personnage = equipe[index]
            print(f"Personnage #{index + 1} : {personnage.nom} - ATK: {personnage.atk}, DEF: {personnage.defense}, PV: {personnage.pv}")
        else:
            print(f"Personnage #{index + 1} : [vide]")
    print()


def _afficher_personnages_disponibles(personnages):
    """Affiche la liste des personnages disponibles"""
    print("--- Personnages disponibles ---")
    for index, personnage in enumerate(personnages, 1):
        print(f"{index}. {personnage.nom} - ATK: {personnage.atk}, DEF: {personnage.defense}, PV: {personnage.pv}")


def _afficher_equipe_finale(equipe):
    """Affiche l'équipe finale avant le début du combat"""
    clear_screen()
    print("\n=== VOTRE ÉQUIPE FINALE ===")
    for index, personnage in enumerate(equipe, 1):
        print(f"Personnage #{index} : {personnage.nom} - ATK: {personnage.atk}, DEF: {personnage.defense}, PV: {personnage.pv}")


def _afficher_entete_vague(numero_vague, monstre):
    """Affiche l'en-tête d'une nouvelle vague"""
    print(f"\n=== Vague {numero_vague} ===")
    print(f"Monstre rencontré : {monstre.nom} - ATK: {monstre.atk}, DEF: {monstre.defense}, PV: {monstre.pv}")


def _equipe_a_survivants(equipe):
    """Vérifie s'il reste au moins un personnage vivant dans l'équipe"""
    return any(personnage.est_vivant() for personnage in equipe)
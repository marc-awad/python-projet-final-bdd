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
        _annuler_initialisation()
        return

    equipe_joueur = _creer_equipe()
    if equipe_joueur is None:
        return

    _demarrer_partie(equipe_joueur, nom_joueur)


def _annuler_initialisation():
    """Annule l'initialisation et retourne au menu"""
    print("Retour au menu principal.")
    time.sleep(DELAY_MESSAGE_COURT)


def _creer_equipe():
    """Crée l'équipe du joueur"""
    personnages_disponibles = get_all_personnages()
    
    if not _valider_personnages_disponibles(personnages_disponibles):
        return None

    equipe = _selectionner_equipe(personnages_disponibles)
    if equipe is None:
        return None

    _afficher_equipe_finale(equipe)
    attendre_entree("\nAppuyez sur Entrée pour commencer le combat...")
    
    return equipe


def _valider_personnages_disponibles(personnages):
    """Vérifie qu'il existe des personnages disponibles"""
    if not personnages:
        print(MSG_AUCUN_PERSONNAGE)
        attendre_entree()
        return False
    return True


def _demarrer_partie(equipe, nom_joueur):
    """Démarre la partie de combat"""
    clear_screen()
    _lancer_combat_par_vagues(equipe, nom_joueur)


def _lancer_combat_par_vagues(equipe, nom_joueur):
    """Gère la boucle principale du combat par vagues"""
    numero_vague = 1
    
    while True:
        monstre_actuel = _initialiser_vague(numero_vague)
        
        if monstre_actuel is None:
            break

        if _executer_combat(equipe, monstre_actuel):
            numero_vague = _gerer_victoire_vague(numero_vague, monstre_actuel, equipe)
        else:
            _gerer_defaite(nom_joueur, numero_vague - 1)
            break


def _initialiser_vague(numero_vague):
    """Initialise une nouvelle vague de combat"""
    clear_screen()
    monstre = get_random_monstre()
    
    if not monstre:
        print(MSG_AUCUN_MONSTRE)
        return None
    
    _afficher_entete_vague(numero_vague, monstre)
    return monstre


def _gerer_victoire_vague(numero_vague, monstre, equipe):
    """Gère la victoire d'une vague"""
    print(f"{monstre.nom}{MSG_VICTOIRE}")
    print(f"Vague {numero_vague} terminée !")
    
    # ✅ AJOUTÉ : Restauration des PV
    _restaurer_equipe(equipe)
    attendre_entree("\nAppuyez sur Entrée pour continuer vers la prochaine vague...")
    
    return numero_vague + 1


def _restaurer_equipe(equipe):
    print(f"\n--- Repos et soins ({int(TAUX_RECUPERATION_PV * 100)}% des PV manquants) ---")
    
    for personnage in equipe:
        if personnage.est_vivant():
            pv_avant = personnage.pv
            pv_manquants = personnage.pv_max - personnage.pv
            soins = int(pv_manquants * TAUX_RECUPERATION_PV)
            
            personnage.pv = min(personnage.pv + soins, personnage.pv_max)
            
            if soins > 0:
                print(f"✚ {personnage.nom} récupère {soins} PV ({pv_avant} → {personnage.pv}/{personnage.pv_max})")
            else:
                print(f"✓ {personnage.nom} est déjà en pleine forme ({personnage.pv}/{personnage.pv_max})")
    
    time.sleep(DELAY_MESSAGE_COURT)


def _executer_combat(equipe, monstre):
    """
    Exécute un combat entre l'équipe et le monstre
    Retourne True si l'équipe gagne, False si elle perd
    """
    while monstre.est_vivant() and _equipe_a_survivants(equipe):
        if _tour_equipe(equipe, monstre):
            return True
        
        if monstre.est_vivant():
            _tour_monstre(equipe, monstre)
            afficher_pv(equipe, monstre)

    return False


def _tour_equipe(equipe, monstre):
    """
    Tour d'attaque de l'équipe
    Retourne True si le monstre est vaincu
    """
    for personnage in equipe:
        if not personnage.est_vivant():
            continue
        
        _attaque_personnage(personnage, monstre)
        
        if not monstre.est_vivant():
            return True
    
    return False


def _attaque_personnage(personnage, monstre):
    """Un personnage attaque le monstre"""
    degats = personnage.attaquer(monstre)
    print(f"{personnage.nom} attaque {monstre.nom} => {degats} dégâts (PV monstre: {monstre.pv})")
    time.sleep(DELAY_ATTAQUE_PERSONNAGE)


def _tour_monstre(equipe, monstre):
    """Le monstre attaque un personnage vivant au hasard"""
    cible = _choisir_cible_aleatoire(equipe)
    degats = monstre.attaquer(cible)
    
    _afficher_attaque_monstre(monstre, cible, degats)


def _choisir_cible_aleatoire(equipe):
    """Choisit une cible vivante au hasard dans l'équipe"""
    cibles_vivantes = [p for p in equipe if p.est_vivant()]
    return random.choice(cibles_vivantes)


def _afficher_attaque_monstre(monstre, cible, degats):
    """Affiche l'attaque du monstre"""
    print(f"{monstre.nom} attaque {cible.nom} => {degats} dégâts (PV restant: {cible.pv})")
    time.sleep(DELAY_ATTAQUE_MONSTRE)


def _gerer_defaite(nom_joueur, vagues_completees):
    """Gère la défaite : sauvegarde le score et affiche le classement"""
    print(f"\n{MSG_DEFAITE}")
    sauvegarder_score(nom_joueur, vagues_completees)
    
    _afficher_classement_final()


def _afficher_classement_final():
    """Affiche le classement final après une défaite"""
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
        _afficher_etat_selection(equipe, personnages_disponibles)
        
        choix = _demander_choix_personnage(len(equipe), len(personnages_disponibles))
        
        if choix == MENU_ANNULER:
            return _annuler_selection()
        
        if not _ajouter_personnage_equipe(equipe, personnages_disponibles, choix):
            continue
    
    return equipe


def _afficher_etat_selection(equipe, personnages_disponibles):
    """Affiche l'état actuel de la sélection d'équipe"""
    _afficher_equipe_en_construction(equipe)
    _afficher_personnages_disponibles(personnages_disponibles)


def _demander_choix_personnage(index_personnage, nb_personnages):
    """Demande au joueur de choisir un personnage"""
    numero_personnage = index_personnage + 1
    return saisir_entier(
        f"\nSélectionnez le personnage #{numero_personnage} (1-{nb_personnages}, 0 pour annuler) : ",
        valeur_min=MENU_ANNULER,
        valeur_max=nb_personnages
    )


def _annuler_selection():
    """Annule la sélection d'équipe"""
    print("Sélection annulée. Retour au menu.")
    time.sleep(DELAY_MESSAGE_COURT)
    return None


def _ajouter_personnage_equipe(equipe, personnages_disponibles, choix):
    """
    Ajoute un personnage à l'équipe si valide
    Retourne True si ajouté, False sinon
    """
    personnage_choisi = personnages_disponibles[choix - 1]
    
    if personnage_choisi in equipe:
        _afficher_personnage_deja_choisi()
        return False
    
    equipe.append(personnage_choisi)
    _confirmer_ajout_personnage(personnage_choisi)
    return True


def _afficher_personnage_deja_choisi():
    """Affiche un message si le personnage est déjà choisi"""
    print("Personnage déjà choisi, choisissez un autre.")
    time.sleep(DELAY_MESSAGE_COURT)


def _confirmer_ajout_personnage(personnage):
    """Confirme l'ajout d'un personnage à l'équipe"""
    print(f"\n✓ {personnage.nom} ajouté à l'équipe !")
    time.sleep(DELAY_MESSAGE_COURT)


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
            _afficher_personnage_selectionne(equipe[index], index)
        else:
            _afficher_slot_vide(index)
    
    print()


def _afficher_personnage_selectionne(personnage, index):
    """Affiche un personnage sélectionné"""
    print(f"Personnage #{index + 1} : {personnage.nom} - ATK: {personnage.atk}, DEF: {personnage.defense}, PV: {personnage.pv}")


def _afficher_slot_vide(index):
    """Affiche un slot vide dans l'équipe"""
    print(f"Personnage #{index + 1} : [vide]")


def _afficher_personnages_disponibles(personnages):
    """Affiche la liste des personnages disponibles"""
    print("--- Personnages disponibles ---")
    
    for index, personnage in enumerate(personnages, 1):
        _afficher_info_personnage(index, personnage)


def _afficher_info_personnage(index, personnage):
    """Affiche les informations d'un personnage"""
    print(f"{index}. {personnage.nom} - ATK: {personnage.atk}, DEF: {personnage.defense}, PV: {personnage.pv}")


def _afficher_equipe_finale(equipe):
    """Affiche l'équipe finale avant le début du combat"""
    clear_screen()
    print("\n=== VOTRE ÉQUIPE FINALE ===")
    
    for index, personnage in enumerate(equipe, 1):
        _afficher_info_personnage(index, personnage)


def _afficher_entete_vague(numero_vague, monstre):
    """Affiche l'en-tête d'une nouvelle vague"""
    print(f"\n=== Vague {numero_vague} ===")
    print(f"Monstre rencontré : {monstre.nom} - ATK: {monstre.atk}, DEF: {monstre.defense}, PV: {monstre.pv}")


def _equipe_a_survivants(equipe):
    """Vérifie s'il reste au moins un personnage vivant dans l'équipe"""
    return any(personnage.est_vivant() for personnage in equipe)
import time
from utils import clear_screen, attendre_entree, get_all_personnages, saisir_entier
from constants import (
    MSG_AUCUN_PERSONNAGE,
    NB_PERSONNAGES_EQUIPE,
    MENU_ANNULER,
    DELAY_MESSAGE_COURT,
)


def saisir_nom_joueur():
    """Demande au joueur de saisir son nom"""
    while True:
        nom = input("Entrez votre nom (0 pour annuler) : ").strip()

        if nom == "0":
            return None

        if nom:
            return nom

        print("Nom invalide. Réessayez.")


def creer_equipe():
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


def _selectionner_equipe(personnages_disponibles):
    """Permet au joueur de sélectionner son équipe de personnages"""
    equipe = []
    disponibles = personnages_disponibles.copy()

    while len(equipe) < NB_PERSONNAGES_EQUIPE:
        clear_screen()
        _afficher_etat_selection(equipe, disponibles)

        choix = _demander_choix_personnage(len(equipe), len(disponibles))

        if choix == MENU_ANNULER:
            return _annuler_selection()

        personnage_choisi = disponibles.pop(choix - 1)
        equipe.append(personnage_choisi)

        _confirmer_ajout_personnage(personnage_choisi)

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
        valeur_max=nb_personnages,
    )


def _annuler_selection():
    """Annule la sélection d'équipe"""
    print("Sélection annulée. Retour au menu.")
    time.sleep(DELAY_MESSAGE_COURT)
    return None


def _confirmer_ajout_personnage(personnage):
    """Confirme l'ajout d'un personnage à l'équipe"""
    print(f"\n✓ {personnage.nom} ajouté à l'équipe !")
    time.sleep(DELAY_MESSAGE_COURT)


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
    print(
        f"Personnage #{index + 1} : {personnage.nom} - ATK: {personnage.atk}, DEF: {personnage.defense}, PV: {personnage.pv}"
    )


def _afficher_slot_vide(index):
    """Affiche un slot vide dans l'équipe"""
    print(f"Personnage #{index + 1} : [vide]")


def _afficher_personnages_disponibles(personnages):
    """Affiche la liste des personnages disponibles"""
    print("--- Personnages disponibles ---")

    for index, personnage in enumerate(personnages, 1):
        _afficher_info_personnage(index, personnage)


def _afficher_info_personnage(index, personnage):
    print(f"{index}. {personnage}")


def _afficher_equipe_finale(equipe):
    """Affiche l'équipe finale avant le début du combat"""
    clear_screen()
    print("\n=== VOTRE ÉQUIPE FINALE ===")

    for index, personnage in enumerate(equipe, 1):
        _afficher_info_personnage(index, personnage)

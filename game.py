import time
from utils import clear_screen, attendre_entree
from constants import DELAY_MESSAGE_COURT
from team_selection import creer_equipe, saisir_nom_joueur
from combat import lancer_combat_par_vagues


def initialize_game():
    """Point d'entrée du jeu : initialise une nouvelle partie"""
    clear_screen()
    print("Bienvenue dans le jeu de combat par vagues !")

    nom_joueur = saisir_nom_joueur()
    if nom_joueur is None:
        _annuler_initialisation()
        return

    equipe_joueur = creer_equipe()
    if equipe_joueur is None:
        return

    _demarrer_partie(equipe_joueur, nom_joueur)


def _annuler_initialisation():
    """Annule l'initialisation et retourne au menu"""
    print("Retour au menu principal.")
    time.sleep(DELAY_MESSAGE_COURT)


def _demarrer_partie(equipe, nom_joueur):
    """Démarre la partie de combat"""
    clear_screen()
    lancer_combat_par_vagues(equipe, nom_joueur)

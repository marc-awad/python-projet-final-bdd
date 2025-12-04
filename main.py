import time
from utils import (
    get_top_scores, 
    clear_screen, 
    afficher_classement_formate,
    saisir_entier,
    attendre_entree
)
from constants import *
from game import initialize_game
from db import verify_connection, close_connection


def main():
    """Point d'entrée principal de l'application"""
    if not _verifier_prerequis():
        exit(1)
    
    _afficher_message_connexion()
    _executer_boucle_principale()


def _verifier_prerequis():
    """Vérifie que tous les prérequis sont satisfaits"""
    if not verify_connection():
        return False
    return True


def _afficher_message_connexion():
    """Affiche le message de confirmation de connexion"""
    print("Connexion MongoDB établie\n")
    time.sleep(DELAY_MESSAGE_COURT)


def _executer_boucle_principale():
    """Exécute la boucle principale du menu"""
    try:
        menu_principal()
    except KeyboardInterrupt:
        _gerer_interruption()
    except Exception as e:
        _gerer_erreur_inattendue(e)
    finally:
        close_connection()


def menu_principal():
    """Gère le menu principal du jeu"""
    while True:
        clear_screen()
        _afficher_menu()
        
        choix = _demander_choix_menu()
        _traiter_choix_menu(choix)
        
        if _doit_quitter(choix):
            break


def _doit_quitter(choix):
    """Vérifie si l'utilisateur veut quitter"""
    return choix == MENU_QUITTER


def _afficher_menu():
    """Affiche les options du menu principal"""
    print("\n=== MENU PRINCIPAL ===")
    print(f"{MENU_JOUER}. Démarrer le jeu")
    print(f"{MENU_CLASSEMENT}. Classement")
    print(f"{MENU_QUITTER}. Quitter")


def _demander_choix_menu():
    """Demande et retourne le choix de l'utilisateur"""
    return saisir_entier(
        "\nChoisissez une option : ",
        valeur_min=MENU_JOUER,
        valeur_max=MENU_QUITTER
    )


def _traiter_choix_menu(choix):
    """Exécute l'action correspondant au choix du menu"""
    if choix == MENU_JOUER:
        initialize_game()
    elif choix == MENU_CLASSEMENT:
        _afficher_page_classement()
    elif choix == MENU_QUITTER:
        _afficher_message_sortie()


def _afficher_message_sortie():
    """Affiche le message d'au revoir"""
    print(MSG_AU_REVOIR)


def _afficher_page_classement():
    """Affiche la page du classement des scores"""
    try:
        _montrer_classement()
    except Exception as e:
        _gerer_erreur_classement(e)


def _montrer_classement():
    """Récupère et affiche le classement"""
    clear_screen()
    scores = get_top_scores(TOP_SCORES_LIMIT)
    afficher_classement_formate(scores)
    attendre_entree()


def _gerer_erreur_classement(exception):
    """Gère les erreurs lors de l'affichage du classement"""
    print(f"Erreur lors de l'affichage du classement : {exception}")
    attendre_entree()


def _gerer_interruption():
    """Gère l'interruption par Ctrl+C"""
    print(MSG_INTERRUPTION)


def _gerer_erreur_inattendue(exception):
    """Gère les erreurs inattendues"""
    print(f"Erreur inattendue : {exception}")


if __name__ == "__main__":
    main()
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


def menu_principal():
    """Gère le menu principal du jeu"""
    try:
        while True:
            clear_screen()
            _afficher_menu()
            
            choix = saisir_entier(
                "\nChoisissez une option : ",
                valeur_min=MENU_JOUER,
                valeur_max=MENU_QUITTER
            )
            
            _traiter_choix_menu(choix)
            
            if choix == MENU_QUITTER:
                break
                
    except KeyboardInterrupt:
        print(MSG_INTERRUPTION)
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        close_connection()


def _afficher_menu():
    """Affiche les options du menu principal"""
    print("\n=== MENU PRINCIPAL ===")
    print(f"{MENU_JOUER}. Démarrer le jeu")
    print(f"{MENU_CLASSEMENT}. Classement")
    print(f"{MENU_QUITTER}. Quitter")


def _traiter_choix_menu(choix):
    """Exécute l'action correspondant au choix du menu"""
    if choix == MENU_JOUER:
        initialize_game()
    elif choix == MENU_CLASSEMENT:
        _afficher_page_classement()
    elif choix == MENU_QUITTER:
        print(MSG_AU_REVOIR)


def _afficher_page_classement():
    """Affiche la page du classement des scores"""
    try:
        clear_screen()
        scores = get_top_scores(TOP_SCORES_LIMIT)
        afficher_classement_formate(scores)
        attendre_entree()
        
    except Exception as e:
        print(f"Erreur lors de l'affichage du classement : {e}")
        attendre_entree()


if __name__ == "__main__":
    if not verify_connection():
        exit(1)
    
    print("Connexion MongoDB établie\n")
    time.sleep(DELAY_MESSAGE_COURT)
    menu_principal()
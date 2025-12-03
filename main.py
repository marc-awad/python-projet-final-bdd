import time
from utils import get_top_scores, clear_screen
from constants import *
from game import initialize_game

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
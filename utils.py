import os
import random
from db import db
from constants import *
from models import Personnage, Monstre


def get_all_personnages():
    """Récupère tous les personnages depuis la base de données"""
    return _recuperer_entites(COLLECTION_PERSONNAGES, Personnage, "personnage")


def get_random_monstre():
    """Récupère un monstre aléatoire depuis la base de données"""
    entites = _recuperer_entites(COLLECTION_MONSTRES, Monstre, "monstre")
    return random.choice(entites) if entites else None


def get_top_scores(limite=TOP_SCORES_LIMIT):
    """Récupère les meilleurs scores depuis la base de données"""
    try:
        scores_cursor = db[COLLECTION_SCORES].find().sort("vagues", -1).limit(limite)
        return list(scores_cursor)
    except Exception as e:
        _afficher_erreur_db("récupération des scores", e)
        return []


def afficher_pv(equipe, monstre):
    """Affiche les PV actuels de toute l'équipe et du monstre"""
    for personnage in equipe:
        print(f"{personnage.nom} - PV: {personnage.pv}/{personnage.pv_max}")
    print(f"{monstre.nom} - PV: {monstre.pv}/{monstre.pv_max}")


def clear_screen():
    """Efface l'écran du terminal (Windows et Unix)"""
    os.system('cls' if os.name == 'nt' else 'clear')


def sauvegarder_score(nom_joueur, nombre_vagues):
    """Enregistre le score du joueur dans la base de données"""
    try:
        db[COLLECTION_SCORES].insert_one({
            "joueur": nom_joueur, 
            "vagues": nombre_vagues
        })
        print(f"Votre score de {nombre_vagues} vagues a été enregistré !")
    except Exception as e:
        _afficher_erreur_db("sauvegarde du score", e)


def afficher_classement_formate(scores):
    """Affiche le classement de manière formatée"""
    if not scores:
        print("Aucun score disponible.")
        return
    
    print("\n=== TOP 3 DES SCORES ===")
    print(f"{'Rang':<{LARGEUR_RANG}}{'Joueur':<{LARGEUR_JOUEUR}}{'Vagues':<{LARGEUR_VAGUES}}")
    print("-" * (LARGEUR_RANG + LARGEUR_JOUEUR + LARGEUR_VAGUES))
    
    for rang, score in enumerate(scores, start=1):
        print(f"{rang:<{LARGEUR_RANG}}{score['joueur']:<{LARGEUR_JOUEUR}}{score['vagues']:<{LARGEUR_VAGUES}}")


def saisir_entier(message_prompt, valeur_min=None, valeur_max=None):
    """Demande à l'utilisateur de saisir un entier avec validation"""
    while True:
        saisie = input(message_prompt).strip()
        
        if not saisie.isdigit():
            print(MSG_ENTREE_INVALIDE)
            continue
        
        valeur = int(saisie)
        
        # Validation des bornes si spécifiées
        if valeur_min is not None and valeur < valeur_min:
            print(f"Valeur trop petite. Minimum : {valeur_min}")
            continue
        
        if valeur_max is not None and valeur > valeur_max:
            print(f"Valeur trop grande. Maximum : {valeur_max}")
            continue
        
        return valeur


def attendre_entree(message=MSG_RETOUR_MENU):
    """Fait une pause jusqu'à ce que l'utilisateur appuie sur Entrée"""
    input(message)


# Fonctions privées (helper functions)

def _recuperer_entites(nom_collection, classe_entite, type_entite):
    """Récupère des entités depuis la base de données et les instancie"""
    try:
        donnees_entites = list(db[nom_collection].find())
        
        if not donnees_entites:
            print(f"Attention : Aucun {type_entite} trouvé dans la base de données.")
            return []
        
        entites = [
            classe_entite(e['nom'], e['atk'], e['defense'], e['pv'])
            for e in donnees_entites
        ]
        return entites
        
    except Exception as e:
        _afficher_erreur_db(f"récupération des {type_entite}s", e)
        return []


def _afficher_erreur_db(operation, exception):
    """Affiche un message d'erreur standardisé pour les problèmes de base de données"""
    print(f"Erreur lors de la {operation} : {exception}")
    print("Veuillez vérifier que MongoDB est démarré et accessible.")
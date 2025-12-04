import os
import random
from db import get_db
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
        return _recuperer_scores_tries(limite)
    except Exception as e:
        _afficher_erreur_db("récupération des scores", e)
        return []


def afficher_pv(equipe, monstre):
    """Affiche les PV actuels de toute l'équipe et du monstre"""
    _afficher_pv_equipe(equipe)
    _afficher_pv_monstre(monstre)


def clear_screen():
    """Efface l'écran du terminal (Windows et Unix)"""
    commande = 'cls' if os.name == 'nt' else 'clear'
    os.system(commande)


def sauvegarder_score(nom_joueur, nombre_vagues):
    """Enregistre le score du joueur dans la base de données"""
    try:
        _enregistrer_score(nom_joueur, nombre_vagues)
        _confirmer_sauvegarde(nombre_vagues)
    except Exception as e:
        _afficher_erreur_db("sauvegarde du score", e)


def afficher_classement_formate(scores):
    """Affiche le classement de manière formatée"""
    if not scores:
        _afficher_aucun_score()
        return
    
    _afficher_entete_classement()
    _afficher_lignes_scores(scores)


def saisir_entier(message_prompt, valeur_min=None, valeur_max=None):
    """Demande à l'utilisateur de saisir un entier avec validation"""
    while True:
        saisie = input(message_prompt).strip()
        
        if not _est_entier_valide(saisie):
            print(MSG_ENTREE_INVALIDE)
            continue
        
        valeur = int(saisie)
        
        if _valeur_hors_limites(valeur, valeur_min, valeur_max):
            continue
        
        return valeur


def attendre_entree(message=MSG_RETOUR_MENU):
    """Fait une pause jusqu'à ce que l'utilisateur appuie sur Entrée"""
    input(message)

def _recuperer_entites(nom_collection, classe_entite, type_entite):
    """Récupère des entités depuis la base de données et les instancie"""
    try:
        donnees = list(get_db()[nom_collection].find())
        
        if not donnees:
            _afficher_aucune_entite(type_entite)
            return []
        
        return _creer_instances_entites(donnees, classe_entite)
        
    except Exception as e:
        _afficher_erreur_db(f"récupération des {type_entite}s", e)
        return []


def _creer_instances_entites(donnees, classe_entite):
    """Crée des instances d'entités à partir des données"""
    return [
        classe_entite(e['nom'], e['atk'], e['defense'], e['pv'])
        for e in donnees
    ]


def _recuperer_scores_tries(limite):
    """Récupère les scores triés par ordre décroissant"""
    scores_cursor = get_db()[COLLECTION_SCORES].find().sort("vagues", -1).limit(limite)
    return list(scores_cursor)


def _enregistrer_score(nom_joueur, nombre_vagues):
    """Enregistre un score dans la base de données"""
    get_db()[COLLECTION_SCORES].insert_one({
        "joueur": nom_joueur, 
        "vagues": nombre_vagues
    })

def _afficher_pv_equipe(equipe):
    """Affiche les PV de tous les personnages de l'équipe"""
    for personnage in equipe:
        _afficher_pv_personnage(personnage)


def _afficher_pv_personnage(personnage):
    """Affiche les PV d'un personnage"""
    print(f"{personnage.nom} - PV: {personnage.pv}/{personnage.pv_max}")


def _afficher_pv_monstre(monstre):
    """Affiche les PV du monstre"""
    print(f"{monstre.nom} - PV: {monstre.pv}/{monstre.pv_max}")


def _afficher_aucune_entite(type_entite):
    """Affiche un message quand aucune entité n'est trouvée"""
    print(f"Attention : Aucun {type_entite} trouvé dans la base de données.")


def _afficher_aucun_score():
    """Affiche un message quand aucun score n'est disponible"""
    print("Aucun score disponible.")


def _afficher_entete_classement():
    """Affiche l'en-tête du tableau de classement"""
    print("\n=== TOP 3 DES SCORES ===")
    print(f"{'Rang':<{LARGEUR_RANG}}{'Joueur':<{LARGEUR_JOUEUR}}{'Vagues':<{LARGEUR_VAGUES}}")
    print("-" * (LARGEUR_RANG + LARGEUR_JOUEUR + LARGEUR_VAGUES))


def _afficher_lignes_scores(scores):
    """Affiche toutes les lignes de scores"""
    for rang, score in enumerate(scores, start=1):
        _afficher_ligne_score(rang, score)


def _afficher_ligne_score(rang, score):
    """Affiche une ligne de score"""
    print(f"{rang:<{LARGEUR_RANG}}{score['joueur']:<{LARGEUR_JOUEUR}}{score['vagues']:<{LARGEUR_VAGUES}}")


def _confirmer_sauvegarde(nombre_vagues):
    """Affiche la confirmation de sauvegarde du score"""
    print(f"Votre score de {nombre_vagues} vagues a été enregistré !")


def _afficher_erreur_db(operation, exception):
    """Affiche un message d'erreur standardisé pour les problèmes de base de données"""
    print(f"Erreur lors de la {operation} : {exception}")
    print("Veuillez vérifier que MongoDB est démarré et accessible.")

def _est_entier_valide(saisie):
    """Vérifie si la saisie est un entier valide"""
    return saisie.isdigit()


def _valeur_hors_limites(valeur, valeur_min, valeur_max):
    """
    Vérifie si la valeur est hors limites
    Retourne True si hors limites, False sinon
    """
    if _valeur_trop_petite(valeur, valeur_min):
        return True
    
    if _valeur_trop_grande(valeur, valeur_max):
        return True
    
    return False


def _valeur_trop_petite(valeur, valeur_min):
    """Vérifie si la valeur est inférieure au minimum"""
    if valeur_min is not None and valeur < valeur_min:
        print(f"Valeur trop petite. Minimum : {valeur_min}")
        return True
    return False


def _valeur_trop_grande(valeur, valeur_max):
    """Vérifie si la valeur est supérieure au maximum"""
    if valeur_max is not None and valeur > valeur_max:
        print(f"Valeur trop grande. Maximum : {valeur_max}")
        return True
    return False
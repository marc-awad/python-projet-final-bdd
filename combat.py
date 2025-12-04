import random
import time
from utils import (
    get_random_monstre,
    afficher_pv,
    clear_screen,
    get_top_scores,
    sauvegarder_score,
    afficher_classement_formate,
    attendre_entree,
)
from constants import (
    MSG_AUCUN_MONSTRE,
    MSG_VICTOIRE,
    MSG_DEFAITE,
    TAUX_RECUPERATION_PV,
    DELAY_MESSAGE_COURT,
    DELAY_ATTAQUE_PERSONNAGE,
    DELAY_ATTAQUE_MONSTRE,
    TOP_SCORES_LIMIT,
)


def lancer_combat_par_vagues(equipe, nom_joueur):
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

    _restaurer_equipe(equipe)
    attendre_entree("\nAppuyez sur Entrée pour continuer vers la prochaine vague...")

    return numero_vague + 1


def _restaurer_equipe(equipe):
    """Restaure les PV de l'équipe après une vague"""
    print(
        f"\n--- Repos et soins ({int(TAUX_RECUPERATION_PV * 100)}% des PV manquants) ---"
    )

    for personnage in equipe:
        if personnage.est_vivant():
            pv_avant = personnage.pv
            pv_manquants = personnage.pv_max - personnage.pv
            soins = int(pv_manquants * TAUX_RECUPERATION_PV)

            personnage.pv = min(personnage.pv + soins, personnage.pv_max)

            if soins > 0:
                print(
                    f"✚ {personnage.nom} récupère {soins} PV ({pv_avant} → {personnage.pv}/{personnage.pv_max})"
                )
            else:
                print(
                    f"✓ {personnage.nom} est déjà en pleine forme ({personnage.pv}/{personnage.pv_max})"
                )

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
    print(
        f"{personnage.nom} attaque {monstre.nom} => {degats} dégâts (PV monstre: {monstre.pv})"
    )
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
    print(
        f"{monstre.nom} attaque {cible.nom} => {degats} dégâts (PV restant: {cible.pv})"
    )
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


def _afficher_entete_vague(numero_vague, monstre):
    """Affiche l'en-tête d'une nouvelle vague"""
    print(f"\n=== Vague {numero_vague} ===")
    print(
        f"Monstre rencontré : {monstre.nom} - ATK: {monstre.atk}, DEF: {monstre.defense}, PV: {monstre.pv}"
    )


def _equipe_a_survivants(equipe):
    """Vérifie s'il reste au moins un personnage vivant dans l'équipe"""
    return any(personnage.est_vivant() for personnage in equipe)

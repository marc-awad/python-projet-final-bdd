class Entity:
    """Classe de base pour les personnages et monstres"""
    
    def __init__(self, nom, atk, defense, pv):
        self.nom = nom
        self.atk = atk
        self.defense = defense
        self.pv = pv
        self.pv_max = pv

    def attaquer(self, cible):
        """Calcule les dégâts en tenant compte de la défense et les inflige à la cible"""
        degats_bruts = self.atk - cible.defense
        degats_reels = max(degats_bruts, 0)  # Évite les dégâts négatifs
        cible.subir_degats(degats_reels)
        return degats_reels

    def subir_degats(self, valeur_degats):
        """Réduit les PV en s'assurant qu'ils ne deviennent pas négatifs"""
        self.pv = max(self.pv - valeur_degats, 0)

    def est_vivant(self):
        """Vérifie si l'entité a encore des PV"""
        return self.pv > 0

    def __str__(self):
        return f"{self.nom} - ATK: {self.atk}, DEF: {self.defense}, PV: {self.pv}/{self.pv_max}"


class Personnage(Entity):
    """Représente un personnage jouable"""
    pass


class Monstre(Entity):
    """Représente un monstre ennemi"""
    pass
class Entity:
    def __init__(self, nom, atk, defense, pv):
        self.nom = nom
        self.atk = atk
        self.defense = defense
        self.pv = pv
        self.pv_max = pv

    def attaquer(self, cible):
        degats = max(self.atk - cible.defense, 0)
        cible.subir_degats(degats)
        return degats

    def subir_degats(self, valeur):
        self.pv -= valeur
        if self.pv < 0:
            self.pv = 0

    def est_vivant(self):
        return self.pv > 0

    def __str__(self):
        return f"{self.nom} - ATK: {self.atk}, DEF: {self.defense}, PV: {self.pv}/{self.pv_max}"


class Personnage(Entity):
    def __init__(self, nom, atk, defense, pv):
        super().__init__(nom, atk, defense, pv)


class Monstre(Entity):
    def __init__(self, nom, atk, defense, pv):
        super().__init__(nom, atk, defense, pv)

class Personnage:
    def __init__(self, nom, atk, defense, pv):
        self.nom = nom
        self.atk = atk
        self.defense = defense
        self.pv = pv

    def __str__(self):
        return f"{self.nom} - ATK: {self.atk}, DEF: {self.defense}, PV: {self.pv}"


class Monstre:
    def __init__(self, nom, atk, defense, pv):
        self.nom = nom
        self.atk = atk
        self.defense = defense
        self.pv = pv

    def __str__(self):
        return f"{self.nom} - ATK: {self.atk}, DEF: {self.defense}, PV: {self.pv}"

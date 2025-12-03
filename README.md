# 🎮 Jeu RPG MongoDB - Combat par Vagues

Un jeu RPG en ligne de commande où vous composez une équipe de 3 héros pour affronter des vagues infinies de monstres. Toutes les données sont stockées dans MongoDB.

## ✨ Fonctionnalités

- 🦸 10 personnages jouables avec statistiques uniques (ATK, DEF, PV)
- 👹 10 types de monstres aléatoires
- ⚔️ Système de combat automatisé avec calcul de dégâts
- 📊 Top 3 des meilleurs scores enregistrés
- 🎯 Compteur de vagues infini

## 🚀 Installation & Lancement

**Prérequis :**

- Python 3.8+
- MongoDB (démarré sur `localhost:27017`)

**Installation :**

```bash
pip install pymongo
```

**Exécution :**

```bash
# 1. Initialiser la base de données
python db_init.py

# 2. Lancer le jeu
python main.py
```

## 🎯 Objectif

Survivez au maximum de vagues et atteignez le Top 3 du classement !

## 📂 Structure

```
python-projet-final-bdd/
├── main.py        # Menu principal
├── game.py        # Logique de combat
├── models.py      # Classes Personnage/Monstre
├── utils.py       # Fonctions utilitaires
├── constants.py   # Constantes du jeu
└── db_init.py     # Initialisation MongoDB
```

## 🎮 Gameplay

1. Choisissez votre nom de joueur
2. Composez une équipe de 3 personnages uniques
3. Affrontez des monstres vague après vague
4. Chaque victoire incrémente votre score
5. Game over quand toute votre équipe est KO

---

_Développé en Python avec MongoDB_

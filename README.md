# 🎮 Jeu RPG MongoDB - Combat par Vagues

Un jeu RPG en ligne de commande où vous composez une équipe de 3 héros pour affronter des vagues infinies de monstres. Toutes les données sont stockées dans MongoDB.

## ✨ Fonctionnalités

- 🦸 10 personnages jouables avec statistiques uniques (ATK, DEF, PV)
- 👹 10 types de monstres aléatoires
- ⚔️ Système de combat automatisé avec calcul de dégâts
- 💚 Restauration partielle des PV entre les vagues
- 📊 Top 10 des meilleurs scores enregistrés dans MongoDB
- 🎯 Compteur de vagues infini avec difficulté progressive

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

Survivez au maximum de vagues et atteignez le Top du classement !

## 📂 Structure du Projet

```
python-projet-final-bdd/
├── main.py              # Menu principal et point d'entrée
├── game.py              # Orchestration du jeu
├── team_selection.py    # Sélection et création d'équipe
├── combat.py            # Logique de combat et gestion des vagues
├── models.py            # Classes Personnage/Monstre
├── utils.py             # Fonctions utilitaires (affichage, saisie, scores)
├── constants.py         # Constantes et paramètres du jeu
├── db.py                # Configuration MongoDB
└── db_init.py           # Initialisation de la base de données
```

## 🎮 Gameplay

1. **Saisie du nom** - Entrez votre nom de joueur
2. **Composition d'équipe** - Choisissez 3 personnages uniques parmi 10 héros disponibles
3. **Combat par vagues** - Affrontez des monstres de plus en plus puissants
4. **Repos** - Récupérez une partie de vos PV entre chaque vague
5. **Game Over** - La partie se termine quand toute votre équipe est KO
6. **Classement** - Consultez votre position dans le Top des scores

## 🛠️ Technologies

- **Python 3.8+** - Langage de programmation
- **MongoDB** - Base de données NoSQL pour le stockage des personnages, monstres et scores
- **PyMongo** - Driver MongoDB pour Python

---

_Projet développé dans le cadre d'un exercice Python avec MongoDB_

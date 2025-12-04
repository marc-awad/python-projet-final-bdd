# Configuration MongoDB
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "jeu_video"

# Noms des collections
COLLECTION_PERSONNAGES = "personnages"
COLLECTION_MONSTRES = "monstres"
COLLECTION_SCORES = "scores"

# Configuration de l'équipe
NB_PERSONNAGES_EQUIPE = 3
TOP_SCORES_LIMIT = 3

# Configuration du gameplay
TAUX_RECUPERATION_PV = 0.6

# Délais d'affichage pour améliorer la lisibilité
DELAY_ATTAQUE_PERSONNAGE = 0.6
DELAY_ATTAQUE_MONSTRE = 0.3
DELAY_MESSAGE_COURT = 1.0

# Messages
MSG_VICTOIRE = " est vaincu !"
MSG_DEFAITE = "Tous vos personnages sont morts. Défaite !"
MSG_AUCUN_PERSONNAGE = "Aucun personnage disponible. Retour au menu."
MSG_AUCUN_MONSTRE = "Aucun monstre disponible."
MSG_INTERRUPTION = "\n\nInterruption détectée. Au revoir !"
MSG_AU_REVOIR = "Au revoir !"
MSG_ENTREE_INVALIDE = "Entrée invalide. Veuillez entrer un nombre."
MSG_RETOUR_MENU = "\nAppuyez sur Entrée pour revenir au menu..."

# Choix du menu
MENU_JOUER = 1
MENU_CLASSEMENT = 2
MENU_QUITTER = 3
MENU_ANNULER = 0

# Formatage du classement
LARGEUR_RANG = 5
LARGEUR_JOUEUR = 15
LARGEUR_VAGUES = 7

# Dégâts minimum infligés
DEGATS_MINIMUM = 5

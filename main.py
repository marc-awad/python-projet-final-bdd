from utils import get_top_scores, get_all_personnages

while True:
    print("\n=== MENU PRINCIPAL ===")
    print("1. Démarrer le jeu")
    print("2. Classement")
    print("3. Quitter")

    choix = input("Choisissez une option : ")

    if choix == "1":
        nom_joueur = input("Entrez votre nom : ").strip()
        while not nom_joueur:
            nom_joueur = input("Nom invalide. Entrez votre nom : ").strip()

        print(f"Bienvenue {nom_joueur}, vous allez maintenant créer votre équipe de 3 personnages.")

        personnages = get_all_personnages()
        print("\nListe des personnages disponibles :")
        for idx, p in enumerate(personnages, 1):
            print(f"{idx}. {p['nom']} - ATK: {p['atk']}, DEF: {p['defense']}, PV: {p['pv']}")

    elif choix == "2":
        scores = get_top_scores()
        if scores:
            for i, s in enumerate(scores, 1):
                print(f"{i}. {s['joueur']} - Vagues : {s['vagues']}")
        else:
            print("Aucun score disponible.")
    elif choix == "3":
        print("Au revoir !")
        break
    else:
        print("Option invalide.")

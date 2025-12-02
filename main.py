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

        # Sélection de l'équipe du joueur
        equipe = []
        while len(equipe) < 3:
            choix_perso = input(f"Sélectionnez le personnage #{len(equipe)+1} (1-{len(personnages)}): ").strip()
            if not choix_perso.isdigit() or int(choix_perso) < 1 or int(choix_perso) > len(personnages):
                print("Choix invalide, réessayez.")
                continue
            perso = personnages[int(choix_perso)-1]
            if perso in equipe:
                print("Personnage déjà choisi, choisissez un autre.")
                continue
            equipe.append(perso)

        print("\nVotre équipe :")
        for p in equipe:
            print(f"{p['nom']} - ATK: {p['atk']}, DEF: {p['defense']}, PV: {p['pv']}")
            
    elif choix == "2":
        scores = get_top_scores()
        if scores:
            print("\nTop 3 des scores :")
            for i, s in enumerate(scores, 1):
                print(f"{i}. {s['joueur']} - Vagues : {s['vagues']}")
        else:
            print("Aucun score disponible.")
    elif choix == "3":
        print("Au revoir !")
        break
    else:
        print("Option invalide.")

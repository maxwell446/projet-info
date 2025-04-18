def connexion1 ():
    import sqlite3
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    idtf = input("quel est votre id ?")
    mot_de_passe_saisi = input("quel est votre mdp?")

    cur.execute("SELECT mdp FROM login WHERE id = ?", (idtf,))

    resultat = cur.fetchone()

    if resultat : 
        mot_de_passe_base = resultat[0]
    
        if mot_de_passe_saisi == mot_de_passe_base:
            print("Connexion réussie")
        else:
            print("Mot de passe incorrect")
    else :
        print(f"Aucun identifiant '{idtf}' trouvé dans la base.")


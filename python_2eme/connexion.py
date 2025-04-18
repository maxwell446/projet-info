def connexion1 (s, p):
    import sqlite3
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()


    cur.execute("SELECT mdp FROM login WHERE id = ?", (s))

    resultat = cur.fetchone()

    if resultat : 
        mot_de_passe_base = resultat[0]
    
        if p == mot_de_passe_base:
            return True
        else:
            return False
    else :
        return False


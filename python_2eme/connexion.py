def connexion1 (s,p):
    import sqlite3
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()


    mot_de_passe_bdd = cur.execute(f"""SELECT mdp FROM login WHERE id = '{s}' """).fetchone()[0]

    if mot_de_passe_bdd : 
        if p == mot_de_passe_bdd:
            return True
        else:
            return False
    else :
        return False

print(connexion1('coucouc', 'david'))
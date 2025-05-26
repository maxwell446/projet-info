def connexion_orga (s,p):
    import sqlite3
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()


    mot_de_passe_bdd = cur.execute(f"""SELECT mdp FROM login_organisateur WHERE id = '{s}' """).fetchone()

    if mot_de_passe_bdd : 
        mot_de_passe_bdd = mot_de_passe_bdd[0]
        if p == mot_de_passe_bdd:
            return True
        else:
            return False
    else :
        return False
    
print(connexion_orga('capitaine', 'capitainez'))


def connexion_capitaine (s,p):
    import sqlite3
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()


    mot_de_passe_bdd = cur.execute(f"""SELECT mdp FROM login_capitaine WHERE id = '{s}' """).fetchone()

    if mot_de_passe_bdd : 
        mot_de_passe_bdd = mot_de_passe_bdd[0]
        if p == mot_de_passe_bdd:
            return True
        else:
            return False
    else :
        return False

def connexion_arbitre (s,p):
    import sqlite3
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()


    mot_de_passe_bdd = cur.execute(f"""SELECT mdp FROM login_arbitre WHERE id = '{s}' """).fetchone()

    if mot_de_passe_bdd : 
        mot_de_passe_bdd = mot_de_passe_bdd[0]
        if p == mot_de_passe_bdd:
            return True
        else:
            return False
    else :
        return False

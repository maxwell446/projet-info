
import sqlite3
def id_existe_pas(k):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()
    
    cur.execute ("""SELECT id FROM login_organisateur WHERE id = ? """, (k,))
    id_bdd=cur.fetchone()

    
    try:
        if id_bdd:
            return False
        else:
            return True
#    except sqlite3.Error as e:
#        print(f"Erreur SQLite : {e}")
#        return False
    finally:
        if conn:
            conn.close()

def nb_id_bdd (k):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    cur.execute ("""SELECT COUNT(*) FROM login_organisateur""")
    nb_id = cur.fetchone()[0]

    return nb_id


def inscription_login_orga (s, p):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    if nb_id_bdd(k=s) == 0 :
        if id_existe_pas(k=s):
            cur.execute ("""INSERT INTO login_organisateur Values (?,?)""", (s,p))
            conn.commit()
        conn.close()
    else :
        ValueError


def inscription_login_arbitre (s, p):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    if id_existe_pas(k=s):
        cur.execute ("""INSERT INTO login_arbitre Values (?,?)""", (s,p))
        conn.commit()
    conn.close()

def inscription_login_capitaine (s, p):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    if id_existe_pas(k=s):
        cur.execute ("""INSERT INTO login_capitaine Values (?,?)""", (s,p))
        conn.commit()
    conn.close()

def inscription_capitaine (n,p,e):
    import sqlite3
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    cur.execute(""" INSERT INTO Equipe (nom, nbjoueur) VALUES (?, ?)""", (e, 1))
    id_Equipe = cur.lastrowid 
    conn.commit()

    cur.execute("""
                INSERT INTO joueur (nom, prenom, idEquipe) 
                VALUES (?,?,?)
                """, (n,p, id_Equipe))
    conn.commit()

    conn.close()

def inscription_joueur (n,p,i):
    import sqlite3
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    cur.execute(""" INSERT INTO joueur Values (?,?,?)""", (n,p,i))
    cur.execute(""" UPDATE Equipe Set nbJoueur  = nbJoueur + 1 WHERE idEquipe = ?""", (i,) )
    conn.commit()
    
    cur.execute("""
                SELECT joueur.nom, joueur.prenom, Equipe.nom
                FROM joueur
                JOIN Equipe ON joueur.idEquipe = Equipe.idEquipe
                """ )
    conn.commit()
    conn.close()



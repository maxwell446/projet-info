
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

def nb_id_bdd_orga ():
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    cur.execute ("""SELECT COUNT(*) FROM login_organisateur""")
    nb_id = cur.fetchone()[0]

    return nb_id


def inscription_login_orga (s, p):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    
    if id_existe_pas(k=s):
        cur.execute ("""INSERT INTO login_organisateur Values (?,?)""", (s,p))
        conn.commit()
    conn.close()


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

    cur.execute("SELECT idEquipe FROM Equipe WHERE idEquipe = ?", (i,))
    if not cur.fetchone():
        print(f"Erreur : L'équipe avec l'ID {i} n'existe pas.")
        return False

    cur.execute(""" INSERT INTO joueur Values (?,?,?)""", (n,p,i))
    cur.execute(""" UPDATE Equipe Set nbJoueur  = nbJoueur + 1 WHERE idEquipe = ?""", (i,) )
    conn.commit()
    
    print(f"Joueur '{p} {n}' inscrit à l'équipe ID {i} avec succès.")
    return True
    conn.close()


print("--- Test d'inscription de Capitaine ---")
id_equipe_A = inscription_capitaine("Doe", "John", "Équipe A")
if id_equipe_A:
    print(f"Équipe A créée avec ID: {id_equipe_A}")
else:
    print("Échec de la création de l'Équipe A.")

id_equipe_B = inscription_capitaine("Smith", "Jane", "Équipe B")
if id_equipe_B:
    print(f"Équipe B créée avec ID: {id_equipe_B}")
else:
    print("Échec de la création de l'Équipe B.")

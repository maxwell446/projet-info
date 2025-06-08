import sqlite3
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATABASE_NAME = os.path.join(PARENT_DIR, 'tournois_de_sport_vf.sqlite')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def connexion_capitaine (identifiant, mdp):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT mdp FROM login_capitaine WHERE id = ?", (identifiant,))
        mot_de_passe_bdd = cur.fetchone()

        if mot_de_passe_bdd :
            mot_de_passe_bdd = mot_de_passe_bdd['mdp'] # Accès par nom de colonne
            if mdp == mot_de_passe_bdd:
                return True
            else:
                return False # Mot de passe incorrect
        else :
            return False # Identifiant non trouvé
    except sqlite3.Error as e:
        print(f"Erreur de connexion capitaine: {e}")
        return False
    finally:
        if conn:
            conn.close()

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
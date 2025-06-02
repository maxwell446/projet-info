import sqlite3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(SCRIPT_DIR, 'tournois_de_sport.sqlite')

def get_db_connection():
    try:
        conn = sqlite3.connect('tournois_de_sport.sqlite')
        conn.row_factory = sqlite3.Row 
        return conn
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données {DATABASE_NAME}: {e}", file=sys.stderr)
        sys.exit(1) 

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


def init_db():
    """
    Initialise le schéma de la base de données (crée les tables si elles n'existent pas).
    """
    print(f"DEBUG: Démarrage de l'initialisation de la base de données à {DATABASE_NAME}.")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Equipe (
                idEquipe INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL UNIQUE,
                nbJoueur NUMERIC DEFAULT 0
            )
        """)
        print("DEBUG: Table 'Equipe' vérifiée/créée.")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS joueur (
                idJoueur INTEGER PRIMARY KEY AUTOINCREMENT,
                prenom TEXT NOT NULL,
                nom TEXT NOT NULL,
                idEquipe INTEGER,
                FOREIGN KEY (idEquipe) REFERENCES Equipe(idEquipe) ON DELETE CASCADE
            )
        """)
        print("DEBUG: Table 'joueur' vérifiée/créée.")
        conn.commit()
        print("DEBUG: Base de données et tables initialisées avec succès.")
    except sqlite3.Error as e:
        print(f"FATAL ERROR: Échec de l'initialisation de la base de données (CREATE TABLE) : {e}", file=sys.stderr)
        conn.rollback()
        sys.exit(1) 
    finally:
        conn.close()
        print("DEBUG: Connexion de init_db fermée.")


def inscription_capitaine(n, p, e):
    conn = get_db_connection()
    cur = conn.cursor()
    id_equipe = None
    try:
        cur.execute("SELECT idEquipe FROM Equipe WHERE nom = ?", (e,))
        if cur.fetchone():
            print(f"Erreur (inscription_capitaine) : L'équipe '{e}' existe déjà.")
            return None
        
        cur.execute(""" INSERT INTO Equipe (nom, nbJoueur) VALUES (?, ?)""", (e, 1))
        id_equipe = cur.lastrowid
        conn.commit()
        
        cur.execute("""
                    INSERT INTO joueur (prenom, nom, idEquipe)
                    VALUES (?,?,?)
                    """, (p, n, id_equipe))
        conn.commit()
        return id_equipe
    except sqlite3.IntegrityError as error:
        print(f"ERROR (inscription_capitaine) : Erreur d'intégrité (nom d'équipe probablement non unique) : {error}", file=sys.stderr)
        conn.rollback()
        return None
    except sqlite3.Error as error:
        print(f"ERROR (inscription_capitaine) : Erreur SQLite : {error}", file=sys.stderr)
        conn.rollback()
        return None
    except Exception as error:
        print(f"ERROR (inscription_capitaine) : Erreur inattendue : {error}", file=sys.stderr)
        conn.rollback()
        return None
    finally:
        conn.close()

def inscription_joueur(n, p, i):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT idEquipe FROM Equipe WHERE idEquipe = ?", (i,))
        if not cur.fetchone():
            print(f"Erreur (inscription_joueur) : L'équipe avec l'ID {i} n'existe pas.", file=sys.stderr)
            return False

        cur.execute(""" INSERT INTO joueur (prenom, nom, idEquipe) VALUES (?,?,?)""", (p, n, i))
       
        cur.execute(""" UPDATE Equipe SET nbJoueur = nbJoueur + 1 WHERE idEquipe = ?""", (i,) )
        conn.commit()

        print(f"Joueur '{p} {n}' inscrit à l'équipe ID {i} avec succès.")
        return True
    except sqlite3.Error as error:
        print(f"ERROR (inscription_joueur) : Erreur SQLite : {error}", file=sys.stderr)
        conn.rollback()
        return False
    except Exception as error:
        print(f"ERROR (inscription_joueur) : Erreur inattendue lors de l'inscription du joueur : {error}", file=sys.stderr)
        conn.rollback()
        return False
    finally:
        conn.close()
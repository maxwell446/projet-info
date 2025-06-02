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


def inscription_capitaine(nom_capitaine, prenom_capitaine, nom_equipe):
    conn = None 
    id_equipe = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        
        cursor.execute("SELECT idEquipe FROM Equipe WHERE nom = ?", (nom_equipe,))
        equipe_existante = cursor.fetchone()

        if equipe_existante:
            print(f"L'équipe '{nom_equipe}' existe déjà.")
            return None 

        cursor.execute("INSERT INTO Equipe (nom) VALUES (?)", (nom_equipe,))
        id_equipe = cursor.lastrowid 

        cursor.execute(
            "INSERT INTO Capitaine (nom, prenom, idEquipe) VALUES (?, ?, ?)",
            (nom_capitaine, prenom_capitaine, id_equipe)
        )
        conn.commit() 
        print(f"Capitaine '{prenom_capitaine} {nom_capitaine}' et équipe '{nom_equipe}' inscrits avec ID équipe: {id_equipe}")
        return id_equipe 

    except sqlite3.IntegrityError as e:
        print(f"Erreur d'intégrité lors de l'inscription : {e}")
        if conn:
            conn.rollback() 
        return None
    except Exception as e:
        print(f"Une erreur inattendue est survenue lors de l'inscription du capitaine et de l'équipe : {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close() 
    return None 

def inscription_joueur(nom_joueur, prenom_joueur, id_equipe):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Joueur (nom, prenom, idEquipe) VALUES (?, ?, ?)",
            (nom_joueur, prenom_joueur, id_equipe)
        )
        conn.commit()
        print(f"Joueur '{prenom_joueur} {nom_joueur}' inscrit dans l'équipe {id_equipe}")
        return True 
    except Exception as e:
        print(f"Erreur lors de l'inscription du joueur '{prenom_joueur} {nom_joueur}': {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
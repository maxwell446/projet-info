import sqlite3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)  # Obtient le dossier parent
DATABASE_NAME = os.path.join(PARENT_DIR, 'tournois_de_sport.sqlite')
#modification des lignes audessus pour quil se connecte la bonne bdd et quil la trouve sans la recreer a chaque fois 
#la bonne bdd est:tournois_de_sport avec les _ on e ne met pas espaces!!!!!! grand fou va!!!!!
def get_db_connection():
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        return conn

def id_existe_pas(k):
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()

    cur.execute ("""SELECT id FROM login_organisateur WHERE id = ? """, (k,))
    id_bdd=cur.fetchone()


    try:
        if id_bdd:
            return False
        else:
            return True
    finally:
        if conn:
            conn.close()

def nb_id_bdd_orga ():
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()

    cur.execute ("""SELECT COUNT(*) FROM login_organisateur""")
    nb_id = cur.fetchone()[0]

    return nb_id

def inscription_login_orga (s, p):
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()


    if id_existe_pas(k=s):
        cur.execute ("""INSERT INTO login_organisateur Values (?,?)""", (s,p))
        conn.commit()
    conn.close()


def inscription_login_arbitre (s, p):
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()

    if id_existe_pas(k=s):
        cur.execute ("""INSERT INTO login_arbitre Values (?,?)""", (s,p))
        conn.commit()
    conn.close()

def inscription_login_capitaine (s, p):
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()

    if id_existe_pas(k=s):
        cur.execute ("""INSERT INTO login_capitaine Values (?,?)""", (s,p))
        conn.commit()
    conn.close()

def inscription_capitaine(nom_capitaine, prenom_capitaine, nom_equipe):
    conn = None
    id_equipe = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Equipe (nom) VALUES (?)", (nom_equipe,))
        id_equipe = cursor.lastrowid
        cursor.execute(
            "INSERT INTO Capitaine (nom, prenom, idEquipe) VALUES (?, ?, ?)",
            (nom_capitaine, prenom_capitaine, id_equipe)
        )
        conn.commit()
        print(f"Capitaine '{prenom_capitaine} {nom_capitaine}' et équipe '{nom_equipe}' inscrits avec ID équipe: {id_equipe}")
        return id_equipe
    finally:
        if conn:
            conn.close()

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

## rajout de ces deux def pour recuprer les infos dans la bdd pour les afficher dans la page de confirmation. 
def get_equipe_details(id_equipe):
    conn = None
    equipe_details = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Equipe.idEquipe, Equipe.nom AS nom_equipe, Capitaine.nom AS nom_capitaine, Capitaine.prenom AS prenom_capitaine
            FROM Equipe
            JOIN Capitaine ON Equipe.idEquipe = Capitaine.idCapitaine
            WHERE Equipe.idEquipe = ?
        """, (id_equipe,))
        equipe_details = cursor.fetchone()
    except Exception as e:
        print(f"Erreur lors de la récupération des détails de l'équipe: {e}")
    finally:
        if conn:
            conn.close()
    return equipe_details

def get_joueurs_by_equipe_id(id_equipe):
    conn = None
    joueurs = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nom, prenom FROM Joueur WHERE idEquipe = ?
        """, (id_equipe,))
        joueurs = cursor.fetchall() 
    except Exception as e:
        print(f"Erreur lors de la récupération des joueurs: {e}")
    finally:
        if conn:
            conn.close()
    return joueurs
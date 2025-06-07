import sqlite3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATABASE_NAME = os.path.join(PARENT_DIR, 'tournois_de_sport_vf.sqlite')

def get_db_connection():
    """Établit et retourne une connexion à la base de données."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Permet d'accéder aux colonnes par leur nom (ex: row['nom_colonne'])
    return conn

def id_existe_pas(identifiant, table_name):
    """
    Vérifie si un identifiant existe déjà dans une table de login spécifique.
    Retourne True si l'ID n'existe PAS, False sinon.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM {table_name} WHERE id = ?", (identifiant,))
        result = cursor.fetchone()
        return result is None
    finally:
        if conn:
            conn.close()

def inscription_login_capitaine(identifiant, mdp):
    if not id_existe_pas(identifiant, 'login_capitaine'):
        return False, "Cet identifiant est déjà pris."

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login_capitaine (id, mdp) VALUES (?,?)", (identifiant, mdp))
        conn.commit()
        return True, "Inscription réussie !"
    except sqlite3.Error as e:
        print(f"Erreur lors de l'inscription du login capitaine: {e}")
        return False, "Une erreur est survenue lors de l'inscription du login."
    finally:
        if conn:
            conn.close()

def get_capitaine_equipe_by_login_id(login_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT E.idEquipe
            FROM Equipe AS E
            JOIN Capitaine AS C ON E.idEquipe = C.idEquipe
            WHERE C.idLoginCapitaine = ?
        """, (login_id,))
        result = cursor.fetchone()
        return result['idEquipe'] if result else None
    finally:
        if conn:
            conn.close()

def inscription_capitaine_and_equipe(nom_capitaine, prenom_capitaine, nom_equipe, id_login_capitaine, id_competition_actuelle):
    conn = None
    id_equipe = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if get_capitaine_equipe_by_login_id(id_login_capitaine) is not None:
            return None, f"L'identifiant de connexion '{id_login_capitaine}' a déjà une équipe inscrite."

        cursor.execute("SELECT idEquipe FROM Equipe WHERE nom_equipe = ? AND idCompetition = ?", (nom_equipe, id_competition_actuelle))
        if cursor.fetchone():
            return None, f"Le nom d'équipe '{nom_equipe}' existe déjà dans cette compétition."

        cursor.execute("INSERT INTO Equipe (nom_equipe, idCompetition) VALUES (?, ?)", (nom_equipe, id_competition_actuelle))
        id_equipe = cursor.lastrowid

        cursor.execute(
            "INSERT INTO Capitaine (nom_capitaine, prenom_capitaine, idLoginCapitaine, idEquipe) VALUES (?, ?, ?, ?)",
            (nom_capitaine, prenom_capitaine, id_login_capitaine, id_equipe)
        )
        conn.commit()
        return id_equipe, f"L'équipe '{nom_equipe}' et le capitaine '{prenom_capitaine} {nom_capitaine}' ont été inscrits avec succès !"
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
        return True, f"Joueur '{prenom_joueur} {nom_joueur}' inscrit avec succès."
    except sqlite3.Error as e:
        print(f"Erreur lors de l'inscription du joueur '{prenom_joueur} {nom_joueur}': {e}")
        if conn:
            conn.rollback()
        return False, f"Erreur lors de l'inscription du joueur '{prenom_joueur} {nom_joueur}'."
    finally:
        if conn:
            conn.close()

def get_equipe_details(id_equipe):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Equipe.idEquipe, Equipe.nom_equipe, Capitaine.nom_capitaine, Capitaine.prenom_capitaine
            FROM Equipe
            LEFT JOIN Capitaine ON Equipe.idEquipe = Capitaine.idEquipe
            WHERE Equipe.idEquipe = ?
        """, (id_equipe,))
        equipe_details = cursor.fetchone()
        return equipe_details
    finally:
        if conn:
            conn.close()

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
        return joueurs
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des joueurs: {e}")
        return [] # Retourne une liste vide en cas d'erreur
    finally:
        if conn:
            conn.close()

def get_competition_details(id_competition):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Competition WHERE idCompetition = ?", (id_competition,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des détails de la compétition: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_competition_details(id_competition):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Competition WHERE idCompetition = ?", (id_competition,))
        return cursor.fetchone()
    finally:
        if conn:
            conn.close()

def get_all_teams_in_competition(id_competition):
    conn = None
    teams = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT idEquipe, nom_equipe FROM Equipe WHERE idCompetition = ?", (id_competition,))
        teams = cursor.fetchall()
        return teams
    finally:
        if conn:
            conn.close()

def miseajour_statuts_compet(id_competition, new_status): 
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Competition SET etat_competition = ? WHERE idCompetition = ?", (new_status, id_competition))
        conn.commit()
        return True, "Statut de la compétition mis à jour avec succès."
    finally:
        if conn:
            conn.close()



def create_competition(nom_competition, joueur_max):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Competition (nom_competition, nombre_max_equipe, etat_competition) VALUES (?, ?, ?)",
                       (nom_competition, joueur_max, 0))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la compétition: {e}")
        return None
    finally:
        if conn:
            conn.close()

create_competition("les choupis", 10)
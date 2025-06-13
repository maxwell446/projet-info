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

def nb_id_bdd_orga ():
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()

    cur.execute ("""SELECT COUNT(*) FROM login_organisateur""")
    nb_id = cur.fetchone()[0]

    return nb_id

def inscription_login_orga (s, p):
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()

    if nb_id_bdd_orga()==0:


        if id_existe_pas(s, 'login_organisateur')==True:
            cur.execute ("""INSERT INTO login_organisateur Values (?,?)""", (s,p))
            conn.commit()
            conn.close()
            return True
        else : 
            return False
    else :
        return False


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

"""
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
"""


def get_nb_equipe_in_competition(id_competition):
    conn = None
    nb_equipe = 0
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM Equipe WHERE idCompetition = ?", (id_competition,))

        resultat_compte = cur.fetchone()
        if resultat_compte:
            nb_equipe = resultat_compte[0]
        else:
            nb_equipe = 0 

        return nb_equipe
    except sqlite3.Error as e: 
        print(f"Erreur SQLite lors de la récupération du nombre d'équipes: {e}")
        return -1
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

#create_competition("les choupis", 10)

def get_all_competition():
    conn = None
    competition = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT idCompetition, nom_competition FROM Competition")
        competition = cursor.fetchall()
        return competition
    finally:
        if conn:
            conn.close()

import sqlite3

def get_db_connection():
    db_path = "tournois_de_sport_vf.sqlite"  # Assurez-vous que le chemin est correct
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Important pour accéder par nom de colonne
    return conn

def get_all_teams_in_competition(id_competition):
    conn = None
    nom_equipes_list = [] # Initialisation pour stocker uniquement les noms
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # La requête SELECT est correcte pour récupérer l'ID et le nom
        cursor.execute("SELECT IDequipe, nom_equipe FROM Equipe WHERE idCompetition = ?", (id_competition,))
        
        # Récupère toutes les lignes
        teams_data = cursor.fetchall() 
        
        # Itérer sur les données récupérées pour extraire seulement le nom
        for team_row in teams_data:
            nom_equipes_list.append((team_row['IDequipe'], team_row['nom_equipe']))

            # Si row_factory n'est pas défini, utilisez: nom_equipes_list.append(team_row[1])

        print(f"Équipes pour la compétition {id_competition}: {nom_equipes_list}")
        return nom_equipes_list # Retourne la liste des noms

    except sqlite3.Error as e: # Capture des erreurs SQLite spécifiques
        print(f"Erreur SQLite lors de la récupération des équipes: {e}")
        return [] # Retourne une liste vide en cas d'erreur
    finally:
        if conn:
            conn.close()

#print(get_all_teams_in_competition(1))


def get_id_equipe(liste, rang_de_liste, id_competition):
    conn = None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idEquipe FROM Equipe WHERE nom_equipe = ? AND idCompetition = ?", (liste[rang_de_liste], id_competition))
    id_equipe = cursor.fetchone()
    return id_equipe



def generer_calendrier_competition(id_competition):
    """
    Récupère le nombre maximum d'équipes pour une compétition donnée par son ID,
    puis génère un calendrier de matchs en round-robin pour ce nombre d'équipes.
    """
    try:
        nombre_equipe = get_nb_equipe_in_competition(id_competition)

        if nombre_equipe == 0:
            print(f"Erreur : Aucune equipe dans la competition pour le moment dans la competition {id_competition}")
            return None

        equipes = get_all_teams_in_competition(id_competition)

        n = len(equipes)
        if n % 2 != 0:
            equipes.append("BYE") # Ajoutez une équipe fictive pour les nombres impairs
            n += 1

        calendrier = []
        
        for i in range(n - 1): # n-1 journées pour un nombre pair d'équipes
            journee = []
            
            # Match de l'équipe fixe (equipes[0])
            journee.append([[equipes[0]], [equipes[n - 1 - i]]]) 

#            , get_id_equipe(equipes, 0, id_competition)
#, get_id_equipe(equipes, n-1-i, id_competition)

            # Matchs des autres équipes
            for j in range(1, n // 2):
                equipe1_idx = (i + j) % (n - 1)
                equipe2_idx = (i + n - 1 - j) % (n - 1)
                
                e1 = equipes[ (1 + equipe1_idx) ] 
                e2 = equipes[ (1 + equipe2_idx) ]
                journee.append([e1, e2])
            
            # Correction pour le cas de N=2 (pour eviter des erreurs d'indices)
            if n == 2:
                journee = [[equipes[0], equipes[1]]]

            # Filtrer les matchs avec "BYE" si N était initialement impair
            matchs_valides = []
            for match in journee:
                if "BYE" not in match:
                    matchs_valides.append(match)
            
            if matchs_valides: # Ajouter la journée seulement s'il y a des matchs valides
                
                calendrier.append(matchs_valides)
        
        return calendrier

    except sqlite3.Error as e:
        print(f"Une erreur SQLite s'est produite : {e}")
        return None

print(generer_calendrier_competition(1))
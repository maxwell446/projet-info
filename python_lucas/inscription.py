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
    finally:
        if conn:
            conn.close()


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


def get_all_team_ids(idCompetition):
    """
    Récupère tous les IDs d'équipe de la table 'Equipe' dans la base de données.

    Returns:
        list: Une liste d'entiers (IDs d'équipe). Retourne une liste vide en cas d'erreur ou si aucune équipe n'est trouvée.
    """
    conn = None
    team_ids = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT idEquipe FROM Equipe WHERE idcompetition = {idCompetition}")
        results = cursor.fetchall() # Récupère une liste de Row objects ou tuples
        
        # Extrait l'ID de chaque Row object/tuple
        for row in results:
            team_ids.append(row['idEquipe']) # Ou row[0] si row_factory n'est pas utilisé
            
    except sqlite3.Error as e:
        print(f"Erreur SQLite lors de la récupération des IDs d'équipe: {e}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")
    finally:
        if conn:
            conn.close()
    return team_ids

#print(get_all_team_ids(1))

def get_all_team_names(idCompetition):
    """
    Récupère tous les noms d'équipe de la table 'Equipe' dans la base de données.

    Returns:
        list: Une liste de chaînes de caractères (noms d'équipe). Retourne une liste vide en cas d'erreur ou si aucune équipe n'est trouvée.
    """
    conn = None
    team_names = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT nom_equipe FROM Equipe WHERE idcompetition = {idCompetition}")
        results = cursor.fetchall()
        
        # Extrait le nom de chaque Row object/tuple
        for row in results:
            team_names.append(row['nom_equipe']) # Ou row[0] si row_factory n'est pas utilisé
            
    except sqlite3.Error as e:
        print(f"Erreur SQLite lors de la récupération des noms d'équipe: {e}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")
    finally:
        if conn:
            conn.close()
    return team_names

print(get_all_team_names(1))

import sqlite3
import math

# Assurez-vous que cette fonction est bien définie et accessible
def get_db_connection():
    db_path = "tournois_de_sport_vf.sqlite" # Chemin vers votre base de données
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Pour accéder aux colonnes par leur nom
    return conn


import sqlite3
import math

# Assurez-vous que cette fonction est bien définie et accessible
def get_db_connection():
    db_path = "tournois_de_sport_vf.sqlite" # Chemin vers votre base de données
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Permet d'accéder aux colonnes par leur nom
    return conn

def inserer_match(id_competition, journee, id_equipe1, score_equipe1, id_equipe2, score_equipe2):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        abb = """
        INSERT INTO Match (idCompetition, journee, idEquipe1, idEquipe2, score1, score2)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        valeur = (id_competition, journee, id_equipe1, id_equipe2, score_equipe1, score_equipe2)

        cursor.execute(abb, valeur)
        conn.commit()
        return True

    except sqlite3.Error as e:
        return False
    finally:
        if conn:
            conn.close()

def generer_calendrier_round_robin(id_competition):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # CORRECTION APPLIQUÉE ICI : On sélectionne directement depuis la table Equipe
        cursor.execute("""
            SELECT idEquipe, nom_equipe
            FROM Equipe
            WHERE idCompetition = ?
            ORDER BY nom_equipe
        """, (id_competition,))
        equipes_db = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erreur SQLite lors de la récupération des équipes pour la compétition {id_competition}: {e}")
        conn.close()
        return []

    conn.close()
    if not equipes_db or len(equipes_db) < 2:
        print(f"La compétition {id_competition} a moins de 2 équipes inscrites. Impossible de générer un calendrier.")
        return []
    equipes_reelles = [{'id': eq['idEquipe'], 'nom': eq['nom_equipe']} for eq in equipes_db]
    teams = list(equipes_reelles) 
    
    if len(teams) % 2 != 0:
        teams.append({'id': None, 'nom': 'Repos'})
    
    num_teams = len(teams)
    calendrier_genere = []
    num_journees = num_teams - 1 

    for journee_idx in range(num_journees):
        journee_actuelle = journee_idx + 1.
        
        # Rotation de la liste (sauf le premier élément)
        if journee_idx > 0:
            last_team = teams.pop()
            teams.insert(1, last_team)

        # Appariement des équipes pour la journée actuelle
        for i in range(num_teams // 2):
            equipe1 = teams[i]
            equipe2 = teams[num_teams - 1 - i]
            
            if equipe1['id'] is not None and equipe2['id'] is not None:
                # Insérer le match dans la BDD
                inserer_match(id_competition, journee_actuelle, equipe1['id'], None, equipe2['id'], None)
                # Ajouter au calendrier à retourner (pour affichage immédiat si besoin)
                calendrier_genere.append({
                    'journee': journee_actuelle,
                    'equipe1_id': equipe1['id'],
                    'equipe1_nom': equipe1['nom'],
                    'equipe2_id': equipe2['id'],
                    'equipe2_nom': equipe2['nom'],

                    'score1': None,
                    'score2': None
                })

    return calendrier_genere
print(generer_calendrier_round_robin(1))

def recuperer_calendrier_match(id_competition):
    """
    Récupère le calendrier d'une compétition avec les noms des équipes,
    en utilisant des requêtes SQL séparées pour une meilleure lisibilité.

    Args:
        id_competition (int): L'ID de la compétition.

    Returns:
        list: Une liste de dictionnaires, où chaque dictionnaire représente un match.
    """
    calendrier_final = []
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql_matchs = "SELECT * FROM Match WHERE idCompetition = ?"
        cursor.execute(sql_matchs, (id_competition,))
        matchs_db = cursor.fetchall()
        if not matchs_db:
            print(f"Aucun match trouvé pour la compétition {id_competition}.")
            return [] 

        for match_row in matchs_db:
            id_equipe1 = match_row['idEquipe1']
            id_equipe2 = match_row['idEquipe2']
            nom_equipe1 = "Nom non trouvé" 
            nom_equipe2 = "Nom non trouvé" 
            sql_nom_equipe1 = "SELECT nom_equipe FROM Equipe WHERE idEquipe = ?"
            cursor.execute(sql_nom_equipe1, (id_equipe1,))
            resultat_equipe1 = cursor.fetchone() # On sait qu'il n'y aura qu'un seul résultat
            if resultat_equipe1:
                nom_equipe1 = resultat_equipe1['nom_equipe']
            sql_nom_equipe2 = "SELECT nom_equipe FROM Equipe WHERE idEquipe = ?"
            cursor.execute(sql_nom_equipe2, (id_equipe2,))
            resultat_equipe2 = cursor.fetchone()
            if resultat_equipe2:
                nom_equipe2 = resultat_equipe2['nom_equipe']
            calendrier_final.append({
                'journee': match_row['journee'],
                'equipe1_id': id_equipe1,
                'equipe1_nom': nom_equipe1,
                'equipe2_id': id_equipe2,
                'equipe2_nom': nom_equipe2,
                'score1': match_row['score1'],
                'score2': match_row['score2']
            })

    except sqlite3.Error as e:
        print(f"Erreur SQLite dans recuperer_calendrier_match: {e}")
    finally:
        if conn:
            conn.close()

    return calendrier_final
print(recuperer_calendrier_match(1))

def ajouter_score(calendrier, journee_cible, id_equipe_cible, score_equipe):
    try :
        for match in calendrier:
        # Vérifie si la journée correspond
            if match['journee'] == journee_cible:
            # Vérifie si l'id_equipe_cible est equipe1_id ou equipe2_id
                if match['equipe1_id'] == id_equipe_cible:
                    match['score1'] = score_equipe
                    return True
                elif match['equipe2_id'] == id_equipe_cible:
                    match['score2'] = score_equipe
                    return True
        return False
    except sqlite3.Error as e:
        return False
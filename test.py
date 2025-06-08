"""
from flask import Flask, render_template, request
from python_2eme.connexion import connexion1
from python_2eme.inscription import inscription_login
"""
from python_lucas.inscription import get_all_teams_in_competition, get_db_connection, get_nb_equipe_in_competition
"""
app = Flask(__name__)

@app.route("/")
def page_html():
    return render_template("index.html")

@app.route("/traitement", methods=["POST"])
def traitement():
    print("Formulaire reçu !")
    nom_utilisateur = request.form.get("nom") # Récupération de la donnée envoyée
    mot_de_passe = request.form.get("mdp")
    inscription_login(nom_utilisateur, mot_de_passe)
    return f"<h2>Bonjour, {nom_utilisateur} !</h2>"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
"""

import sqlite3
"""
# Assuming get_db_connection is defined and correctly connects to your database
def get_db_connection():
    db_path = "tournois_de_sport_vf.sqlite"  # Adjust this path if your DB file is elsewhere
    conn = sqlite3.connect(db_path)
    # Optional: Set row_factory to sqlite3.Row for easier column access
    conn.row_factory = sqlite3.Row 
    return conn
"""
def generer_calendrier_competition(id_competition):
    """
    Récupère le nombre maximum d'équipes pour une compétition donnée par son ID,
    puis génère un calendrier de matchs en round-robin pour ce nombre d'équipes.

    Args:
        id_competition (int): L'ID de la compétition dans la base de données.

    Returns:
        list: Une liste de listes de matchs (chaque sous-liste représente une journée),
              ou None si la compétition n'est pas trouvée ou en cas d'erreur.
    """
    try:
        nombre_max_equipe = get_nb_equipe_in_competition(id_competition)

        if nombre_max_equipe is None:
            print(f"Erreur : Aucune compétition trouvée avec l'ID {id_competition}")
            return None

        # 2. Générer une liste d'équipes fictives pour la planification
        #    Vous devriez idéalement récupérer les vrais noms d'équipes de la DB si elles existent.
        #    Pour cet exemple, nous allons créer des noms génériques.
        equipes = get_all_teams_in_competition(id_competition)
        # 3. Utiliser l'algorithme de génération de calendrier (comme dans la réponse précédente)
        n = len(equipes)
        if n % 2 != 0:
            equipes.append("BYE") # Ajoutez une équipe fictive pour les nombres impairs
            n += 1

        calendrier = []
        
        for i in range(n - 1): # n-1 journées pour un nombre pair d'équipes
            journee = []
            
            # Match de l'équipe fixe (equipes[0])
            journee.append([equipes[0], equipes[n - 1 - i]]) 

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

print("-" *20)
print(generer_calendrier_competition(1))

"""

@app.route('/', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        inscription_login(identifiant, mdp)
    return render_template('page_incrip.html')
"""

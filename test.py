# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# --- Fonction d'aide pour la connexion à la base de données ---
def get_db_connection():
    # Assurez-vous que le chemin vers votre fichier .sqlite est correct
    # Il est recommandé de le placer dans le même dossier que app.py ou dans un sous-dossier 'data'
    db_path = os.path.join(app.root_path, 'tournois_de_sport.sqlite')
    conn = sqlite3.connect(db_path)
    # Permet d'accéder aux colonnes par leur nom (ex: row['nom'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/creer_tournoi_submit2', methods=['POST'])
nom_tournoi = request.form['nom_tournoi']

@app.route('/creer_tournoi_submit', methods=['POST'])
def creer_tournoi_submit():
    if request.method == 'POST':
        nom_tournoi = request.form['nom_tournoi']
        nb_equipe_max = int(request.form['nb_equipe_max'])
        nb_joueur_max_par_equipe = int(request.form['nb_joueur_max']) # Renommé pour plus de clarté
        nb_terrain_dispo = int(request.form['nb_terrain_dispo'])
        temps_match = int(request.form['temps_match'])
        date_tournoi = request.form['date_tournoi']

        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Créer la table Tournoi si elle n'existe pas (recommandé pour lier les données)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tournois (
                idTournoi INTEGER PRIMARY KEY AUTOINCREMENT,
                nomTournoi TEXT NOT NULL UNIQUE, -- UNIQUE pour éviter les doublons de noms
                sport TEXT,
                nbEquipeMax INTEGER,
                nbJoueurMaxParEquipe INTEGER,
                nbTerrainDispo INTEGER,
                tempsMatch INTEGER,
                dateTournoi TEXT
            )
        ''')
        conn.commit() # Sauvegarder la création de la table si elle est nouvelle

        # 2. Insérer les détails du tournoi principal
        try:
            cursor.execute('''
                INSERT INTO Tournois (nomTournoi, sport, nbEquipeMax, nbJoueurMaxParEquipe, nbTerrainDispo, tempsMatch, dateTournoi)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nom_tournoi, sport, nb_equipe_max, nb_joueur_max_par_equipe, nb_terrain_dispo, temps_match, date_tournoi))
            conn.commit()
            tournoi_id = cursor.lastrowid # Récupérer l'ID du tournoi nouvellement inséré
            print(f"Tournoi '{nom_tournoi}' inséré avec l'ID: {tournoi_id}")

            # 3. Insérer les Terrains (Fields)
            # Assurez-vous que votre table 'terrain' a une colonne pour l'ID du tournoi (idTournoi)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS terrain (
                    idTerrain INTEGER PRIMARY KEY AUTOINCREMENT,
                    nomTerrain TEXT,
                    idTournoi INTEGER,
                    FOREIGN KEY (idTournoi) REFERENCES Tournois(idTournoi)
                )
            ''')
            conn.commit() # Sauvegarder la création de la table si elle est nouvelle

            for i in range(1, nb_terrain_dispo + 1):
                cursor.execute("INSERT INTO terrain (nomTerrain, idTournoi) VALUES (?, ?)", (f"Terrain {i}", tournoi_id))
            conn.commit()
            print(f"{nb_terrain_dispo} terrains insérés pour le tournoi '{nom_tournoi}'.")

            # 4. Insérer les Équipes (Teams)
            # Assurez-vous que votre table 'Equipe' a une colonne pour l'ID du tournoi (idTournoi)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Equipe (
                    idEquipe INTEGER PRIMARY KEY AUTOINCREMENT,
                    nomEquipe TEXT,
                    nbJoueursActuels INTEGER DEFAULT 0,
                    idTournoi INTEGER,
                    FOREIGN KEY (idTournoi) REFERENCES Tournois(idTournoi)
                )
            ''')
            conn.commit() # Sauvegarder la création de la table si elle est nouvelle

            for i in range(1, nb_equipe_max + 1):
                cursor.execute("INSERT INTO Equipe (nomEquipe, idTournoi) VALUES (?, ?)", (f"Équipe {i}", tournoi_id))
            conn.commit()
            print(f"{nb_equipe_max} équipes insérées pour le tournoi '{nom_tournoi}'.")

            # Rediriger vers la page principale en passant le nom du tournoi
            # Le nom du tournoi est passé comme paramètre de requête (query parameter)
            return redirect(url_for('page_principale', nom_tournoi=nom_tournoi))

        except sqlite3.IntegrityError as e:
            # Gérer le cas où le nom du tournoi existe déjà (si UNIQUE est activé)
            print(f"Erreur d'intégrité de la base de données : {e}")
            return render_template('erreur.html', message=f"Un tournoi avec le nom '{nom_tournoi}' existe déjà. Veuillez choisir un nom différent.")
        except Exception as e:
            print(f"Une erreur inattendue est survenue : {e}")
            return render_template('erreur.html', message=f"Une erreur est survenue lors de la création du tournoi : {e}")
        finally:
            conn.close()

# --- Route pour la page principale (où le nom du tournoi sera affiché) ---
@app.route('/page_principale')
def page_principale():
    # Récupérer le nom du tournoi depuis les paramètres de requête de l'URL
    # Si 'nom_tournoi' n'est pas présent, utiliser 'Tournoi par défaut'
    nom_tournoi = request.args.get('nom_tournoi', 'Tournoi par défaut')
    # Vous pouvez également récupérer d'autres détails du tournoi depuis la base de données ici
    return render_template('page_principale.html', nom_tournoi=nom_tournoi)

# --- Une page d'erreur simple (optionnel) ---
@app.route('/erreur')
def erreur_page():
    message = request.args.get('message', 'Une erreur est survenue.')
    return render_template('erreur.html', message=message)

# --- Lancer l'application Flask ---
if __name__ == '__main__':
    # Assurez-vous que le dossier 'templates' est au même niveau que app.py
    app.run(debug=True) # debug=True permet le rechargement automatique et les messages d'erreur détaillés
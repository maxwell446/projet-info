import sqlite3
import os

# Nom du fichier de la base de données
DATABASE_NAME = 'tournois_de_sport_vf.sqlite'

def create_database():
    """
    Crée et initialise la base de données SQLite avec toutes les tables nécessaires si elle n'existe pas.
    """
    # Supprime l'ancienne base de données si elle existe pour repartir de zéro.
    # Attention : cette ligne efface toutes les données existantes !
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print(f"L'ancienne base de données '{DATABASE_NAME}' a été supprimée.")

    conn = None
    try:
        # Crée le fichier de la base de données et s'y connecte
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        print(f"Base de données '{DATABASE_NAME}' créée avec succès.")

        # --- Tableaux pour les identifiants et mots de passe ---

        # Table pour les organisateurs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_organisateur (
                id TEXT PRIMARY KEY,
                mdp TEXT NOT NULL
            );
        ''')
        print("Table 'login_organisateur' créée.")

        # Table pour les arbitres
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_arbitre (
                id TEXT PRIMARY KEY,
                mdp TEXT NOT NULL
            );
        ''')
        print("Table 'login_arbitre' créée.")

        # Table pour les capitaines
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_capitaine (
                id TEXT PRIMARY KEY,
                mdp TEXT NOT NULL
            );
        ''')
        print("Table 'login_capitaine' créée.")

        # --- Tableaux pour la structure des tournois ---

        # Table pour les compétitions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Competition (
                idCompetition INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_competition TEXT NOT NULL UNIQUE,
                nombre_max_equipe INTEGER NOT NULL,
                etat_competition INTEGER DEFAULT 0 NOT NULL 
            );
        ''')
        print("Table 'Competition' créée.")

        # Table pour les équipes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Equipe (
                idEquipe INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_equipe TEXT NOT NULL,
                idCompetition INTEGER NOT NULL,
                FOREIGN KEY (idCompetition) REFERENCES Competition(idCompetition)
            );
        ''')
        print("Table 'Equipe' créée.")

        # Table pour les capitaines (informations personnelles)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Capitaine (
                idCapitaine INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_capitaine TEXT NOT NULL,
                prenom_capitaine TEXT NOT NULL,
                idLoginCapitaine TEXT UNIQUE NOT NULL,
                idEquipe INTEGER UNIQUE,
                FOREIGN KEY (idLoginCapitaine) REFERENCES login_capitaine(id),
                FOREIGN KEY (idEquipe) REFERENCES Equipe(idEquipe)
            );
        ''')
        print("Table 'Capitaine' créée.")

        # Table pour les joueurs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Joueur (
                idJoueur INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                idEquipe INTEGER NOT NULL,
                FOREIGN KEY (idEquipe) REFERENCES Equipe(idEquipe)
            );
        ''')
        print("Table 'Joueur' créée.")

        # Table pour les matchs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Match (
                idMatch INTEGER PRIMARY KEY AUTOINCREMENT,
                idCompetition INTEGER NOT NULL,
                journee INTEGER NOT NULL,
                idEquipe1 INTEGER NOT NULL,
                idEquipe2 INTEGER NOT NULL,
                score1 INTEGER,
                score2 INTEGER,
                FOREIGN KEY (idCompetition) REFERENCES Competition(idCompetition),
                FOREIGN KEY (idEquipe1) REFERENCES Equipe(idEquipe),
                FOREIGN KEY (idEquipe2) REFERENCES Equipe(idEquipe)
            );
        ''')
        print("Table 'Match' créée.")

        # Valide toutes les créations de tables
        conn.commit()
        print("\nToutes les tables ont été créées avec succès.")

    except sqlite3.Error as e:
        print(f"Erreur SQLite lors de la création de la base de données : {e}")
    finally:
        # Ferme la connexion à la base de données
        if conn:
            conn.close()
            print("Connexion à la base de données fermée.")

# --- Exécution de la fonction ---
if __name__ == "__main__":
    # Cette partie du code ne s'exécute que si le script est lancé directement
    create_database()
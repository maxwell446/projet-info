import sqlite3
import os

DATABASE_NAME = 'tournois_de_sport_vf.sqlite'

def create_database():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Création de la table login_organisateur
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_organisateur (
                id TEXT PRIMARY KEY,
                mdp TEXT NOT NULL
            );
        ''')

        # Création de la table login_arbitre
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_arbitre (
                id TEXT PRIMARY KEY,
                mdp TEXT NOT NULL
            );
        ''')

        # Création de la table login_capitaine
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_capitaine (
                id TEXT PRIMARY KEY,
                mdp TEXT NOT NULL
            );
        ''')

        # Création de la table Competition
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Competition (
                idCompetition INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_competition TEXT NOT NULL UNIQUE,
                nombre_max_equipe INTEGER NOT NULL,
                etat_competition INTEGER DEFAULT 0
            );
        ''')

        # Création de la table Equipe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Equipe (
                idEquipe INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_equipe TEXT NOT NULL UNIQUE,
                idCompetition INTEGER NOT NULL,
                FOREIGN KEY (idCompetition) REFERENCES Competition(idCompetition)
            );
        ''')

        # Création de la table Capitaine
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

        # Création de la table Joueur
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Joueur (
                idJoueur INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                idEquipe INTEGER NOT NULL,
                FOREIGN KEY (idEquipe) REFERENCES Equipe(idEquipe)
            );
        ''')

        conn.commit()
        print(f"Base de données '{DATABASE_NAME}' créée avec succès (ou déjà existante).")

    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()
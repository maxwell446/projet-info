import sqlite3
import os
import sys

# --- Configuration de la Base de Données ---
# Construit le chemin absolu du fichier de la base de données.
# Ceci garantit que la base de données est toujours recherchée/créée
# au même endroit que le script Python.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(SCRIPT_DIR, 'tournois_de_sport.sqlite')

print(f"DEBUG: Le script est situé dans : {SCRIPT_DIR}")
print(f"DEBUG: Le chemin complet de la base de données est : {DATABASE_NAME}")

def get_db_connection():
    """
    Établit une connexion à la base de données SQLite.
    Affiche des messages en cas de succès/échec de la connexion.
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row # Permet d'accéder aux colonnes par leur nom
        print(f"DEBUG: Connexion à la base de données {DATABASE_NAME} réussie.")
        return conn
    except sqlite3.Error as e:
        print(f"FATAL ERROR: Impossible de se connecter à la base de données {DATABASE_NAME}: {e}", file=sys.stderr)
        sys.exit(1) # Arrête le script si la connexion échoue

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
        sys.exit(1) # Arrête le script si l'initialisation des tables échoue
    finally:
        conn.close()
        print("DEBUG: Connexion de init_db fermée.")


# --- Fonctions d'inscription ---

def inscription_capitaine(n, p, e):
    conn = get_db_connection()
    cur = conn.cursor()
    id_equipe = None

    try:
        cur.execute("SELECT idEquipe FROM Equipe WHERE nom = ?", (e,))
        if cur.fetchone():
            print(f"AVERTISSEMENT (inscription_capitaine) : L'équipe '{e}' existe déjà. Opération annulée.")
            return None

        print(f"DEBUG: Tentative INSERT Equipe : '{e}'...")
        cur.execute(""" INSERT INTO Equipe (nom, nbJoueur) VALUES (?, ?)""", (e, 1))
        id_equipe = cur.lastrowid
        conn.commit()
        print(f"DEBUG: SUCCÈS INSERT Equipe : '{e}', ID: {id_equipe}.")

        print(f"DEBUG: Tentative INSERT joueur : '{p} {n}' pour équipe ID {id_equipe}...")
        cur.execute("""
                    INSERT INTO joueur (prenom, nom, idEquipe)
                    VALUES (?,?,?)
                    """, (p, n, id_equipe))
        conn.commit()
        print(f"DEBUG: SUCCÈS INSERT joueur : '{p} {n}'.")
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
        print(f"DEBUG: Tentative inscription joueur : '{p} {n}' pour équipe ID {i}...")
        cur.execute("SELECT idEquipe FROM Equipe WHERE idEquipe = ?", (i,))
        if not cur.fetchone():
            print(f"ERROR (inscription_joueur) : L'équipe avec l'ID {i} n'existe pas. Inscription annulée.", file=sys.stderr)
            return False

        print(f"DEBUG: Tentative INSERT joueur : '{p} {n}'...")
        cur.execute(""" INSERT INTO joueur (prenom, nom, idEquipe) VALUES (?,?,?)""", (p, n, i))
        print(f"DEBUG: Tentative UPDATE Equipe : nbJoueur pour équipe ID {i}...")
        cur.execute(""" UPDATE Equipe SET nbJoueur = nbJoueur + 1 WHERE idEquipe = ?""", (i,) )
        conn.commit()
        print(f"DEBUG: SUCCÈS inscription joueur : '{p} {n}' et mise à jour équipe ID {i}.")
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


# --- Bloc d'exécution principal pour les tests ---
if __name__ == "__main__":
    print(f"\n--- Démarrage du script d'inscription ---")

    # --- Section critique de gestion du fichier DB ---
    print(f"DEBUG: Vérification de l'existence du fichier DB à : {DATABASE_NAME}")
    if os.path.exists(DATABASE_NAME):
        print(f"DEBUG: Le fichier de base de données '{os.path.basename(DATABASE_NAME)}' existe déjà.")
        print(f"DEBUG: Tentative de suppression du fichier pour un redémarrage propre...")
        try:
            os.remove(DATABASE_NAME)
            print(f"DEBUG: SUCCÈS : Fichier de base de données supprimé : {DATABASE_NAME}")
        except OSError as e:
            print(f"FATAL ERROR: IMPOSSIBLE DE SUPPRIMER LE FICHIER DB : {e}", file=sys.stderr)
            print(f"FATAL ERROR: Cela peut être dû à des problèmes de permissions ou au fichier verrouillé par une autre application (ex: SQLiteStudio ouvert).", file=sys.stderr)
            sys.exit(1) # Quitte le script car l'état de la DB n'est pas garanti
    else:
        print(f"DEBUG: Le fichier de base de données '{os.path.basename(DATABASE_NAME)}' n'existe PAS. Il sera créé par init_db().")

    # Initialisation de la base de données
    init_db()

    print("\n--- Début des tests d'inscription ---")
    id_equipe_A = inscription_capitaine("Doe", "John", "Équipe A")
    if id_equipe_A:
        print(f"Test Capitaine : Équipe A créée avec ID: {id_equipe_A}")
    else:
        print("Test Capitaine : Échec de la création de l'Équipe A.")

    id_equipe_B = inscription_capitaine("Smith", "Jane", "Équipe B")
    if id_equipe_B:
        print(f"Test Capitaine : Équipe B créée avec ID: {id_equipe_B}")
    else:
        print("Test Capitaine : Échec de la création de l'Équipe B.")

    print("\n--- Test d'inscription d'une équipe existante (doit échouer si 'Équipe A' existe déjà) ---")
    id_equipe_A_bis = inscription_capitaine("Autre", "Cap", "Équipe A")
    if id_equipe_A_bis:
        print(f"Test Capitaine : Équipe A (bis) créée avec ID: {id_equipe_A_bis}")
    else:
        print("Test Capitaine : Échec attendu de la création de l'Équipe A (bis).")


    print("\n--- Test d'inscription de joueurs ---")
    # Vérifier si id_equipe_A est défini avant d'essayer de l'utiliser
    if 'id_equipe_A' in locals() and id_equipe_A:
        inscription_joueur("Brown", "Alice", id_equipe_A)
        inscription_joueur("Green", "Bob", id_equipe_A)
    else:
        print("Test Joueur : Impossible d'ajouter des joueurs à l'Équipe A car elle n'a pas été créée ou son ID n'est pas disponible.")

    if 'id_equipe_B' in locals() and id_equipe_B:
        inscription_joueur("White", "Charlie", id_equipe_B)
    else:
        print("Test Joueur : Impossible d'ajouter des joueurs à l'Équipe B car elle n'a pas été créée ou son ID n'est pas disponible.")


    print("\n--- Test d'inscription d'un joueur à une équipe inexistante (doit échouer) ---")
    inscription_joueur("Non", "Existant", 999) # ID qui n'existe probablement pas


    print("\n--- Vérification finale des données ---")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT joueur.prenom, joueur.nom, Equipe.nom AS nom_equipe, Equipe.nbJoueur FROM joueur JOIN Equipe ON joueur.idEquipe = Equipe.idEquipe")
        players_data = cur.fetchall()
        print("Liste des joueurs et leurs équipes :")
        if players_data:
            for player in players_data:
                print(f"  - {player['prenom']} {player['nom']} ({player['nom_equipe']}), NbJoueur Equipe: {player['nbJoueur']}")
        else:
            print("  Aucun joueur trouvé dans la base de données.")

        cur.execute("SELECT nom, nbJoueur FROM Equipe")
        teams_data = cur.fetchall()
        print("\nNombre de joueurs par équipe (table Equipe) :")
        if teams_data:
            for team in teams_data:
                print(f"  - {team['nom']}: {team['nbJoueur']} joueurs")
        else:
            print("  Aucune équipe trouvée dans la base de données.")
    except Exception as e:
        print(f"ERROR: Erreur lors de la vérification finale des données : {e}", file=sys.stderr)
    finally:
        if 'conn' in locals() and conn: # S'assure que conn existe et n'est pas None
            conn.close()

    print("\n--- Fin du script d'inscription ---")
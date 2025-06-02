ef inscription_capitaine(n, p, e):
    conn = get_db_connection()
    cur = conn.cursor()
    id_equipe = None
    try:
        cur.execute("SELECT idEquipe FROM Equipe WHERE nom = ?", (e,))
        if cur.fetchone():
            print(f"Erreur (inscription_capitaine) : L'équipe '{e}' existe déjà.")
            return None
        
        cur.execute(""" INSERT INTO Equipe (nom, nbJoueur) VALUES (?, ?)""", (e, 1))
        id_equipe = cur.lastrowid
        conn.commit()
        
        cur.execute("""
                    INSERT INTO joueur (prenom, nom, idEquipe)
                    VALUES (?,?,?)
                    """, (p, n, id_equipe))
        conn.commit()
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
return none 

def inscription_joueur(n, p, i):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT idEquipe FROM Equipe WHERE idEquipe = ?", (i,))
        if not cur.fetchone():
            print(f"Erreur (inscription_joueur) : L'équipe avec l'ID {i} n'existe pas.", file=sys.stderr)
            return False

        cur.execute(""" INSERT INTO joueur (prenom, nom, idEquipe) VALUES (?,?,?)""", (p, n, i))
       
        cur.execute(""" UPDATE Equipe SET nbJoueur = nbJoueur + 1 WHERE idEquipe = ?""", (i,) )
        conn.commit()

        print(f"Joueur '{p} {n}' inscrit à l'équipe ID {i} avec succès.")
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
    
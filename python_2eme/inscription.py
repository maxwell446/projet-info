
import sqlite3
def id_existe_pas(k):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()
    
    cur.execute ("""SELECT id FROM login_organisateur WHERE id = ? """, (k,))
    id_bdd=cur.fetchone()

    
    try:
        if id_bdd:
            return False
        else:
            return True
#    except sqlite3.Error as e:
#        print(f"Erreur SQLite : {e}")
#        return False
    finally:
        if conn:
            conn.close()

def nb_id_bdd (k):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    cur.execute ("""SELECT COUNT(*) FROM login_organisateur""")
    nb_id = cur.fetchone()[0]

    return nb_id


def inscription_login_orga (s, p):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    if nb_id_bdd(k=s) == 0 :
        if id_existe_pas(k=s):
            cur.execute ("""INSERT INTO login_organisateur Values (?,?)""", (s,p))
            conn.commit()
        conn.close()
    else :
        ValueError


def inscription_login_arbitre (s, p):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    if id_existe_pas(k=s):
        cur.execute ("""INSERT INTO login_arbitre Values (?,?)""", (s,p))
        conn.commit()
    conn.close()

def inscription_login_capitaine (s, p):
    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    if id_existe_pas(k=s):
        cur.execute ("""INSERT INTO login_capitaine Values (?,?)""", (s,p))
        conn.commit()
    conn.close()


print(id_existe_pas(k='KOUKOUC')) 
print(id_existe_pas(k='coucouc'))

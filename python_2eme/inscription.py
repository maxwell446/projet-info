def inscription_login (s, p):
    import sqlite3

    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    cur.execute ("""INSERT INTO login Values (?,?)""", (s,p))
    conn.commit()
    conn.close()

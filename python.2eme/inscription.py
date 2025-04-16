def inscription1 ():
    import sqlite3

    conn = sqlite3.connect('tournois de sport.sqlite')
    cur = conn.cursor()

    s = input("quel est ton id : ")
    p = input("quel est ton mdp : ")

    cur.execute ("""INSERT INTO login Values (?,?)""", (s,p))
    conn.commit()
    conn.close()
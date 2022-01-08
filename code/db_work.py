import sqlite3


def add_to_db(log, pswrd, points):
    con = sqlite3.connect("../pygame_db.db")
    cur = con.cursor()
    cur.execute("""INSERT INTO players(login, password, record)
                   VALUES(?, ?, ?)""", (log, pswrd, points))
    con.commit()


def from_db():
    con = sqlite3.connect("../pygame_db.db")
    cur = con.cursor()
    res = cur.execute("""SELECT * FROM players
                         ORDER BY record DESC""").fetchall()
    return res


def unique_nick(log):
    con = sqlite3.connect("../pygame_db.db")
    cur = con.cursor()
    res = cur.execute("""SELECT login FROM players""").fetchall()
    res = [elem[0] for elem in res]
    return log not in res


def update_points(login, points):
    con = sqlite3.connect("../pygame_db.db")
    cur = con.cursor()
    cur.execute("""UPDATE players
                   SET record = ?
                   WHERE login = ? and record < ?""", (points, login, points))
    con.commit()

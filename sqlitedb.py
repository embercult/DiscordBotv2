import sqlite3


def copen():
    global conn
    global cur
    conn = sqlite3.connect('userdb.sqlite')
    cur = conn.cursor()


def cclose():
    cur.close()


def createtable():
    copen()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users (handle TEXT UNIQUE, usern TEXT UNIQUE, rating INTEGER)''')
    conn.commit()
    cclose()


def adduser(handle,usern,rating):
    copen()
    cur.execute('''INSERT OR REPLACE INTO Users (handle, usern, rating)
                    VALUES (?, ?, ?)''', (handle, usern, rating))
    conn.commit()
    cclose()


def searchuser(usern):
    copen()
    try:
        return cur.execute("SELECT handle FROM Users WHERE usern LIKE ? ", (usern,)).fetchall()[0][0]
    except IndexError:
        return False
    cclose()


def searchid(id):
    copen()
    try:
        return cur.execute("SELECT rating FROM Users WHERE handle LIKE ? ", (id,)).fetchall()[0][0]
    except IndexError:
        return False
    cclose()


def printdb():
    copen()
    x = []
    for row in cur.execute('SELECT * FROM Users'):
        x.append([str(row[0]), str(row[1]) , row[2]])
    return x
    cclose()

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

def printall():
    copen()
    sqlstr = 'SELECT * FROM Users'
    for row in cur.execute(sqlstr):
        print(str(row[0]), row[1], row[2])
    cclose()

import sqlite3
import dropbox
import os
token1 = str(os.environ.get('TOKENDB', 3))
dbx = dropbox.Dropbox(token1)
dbx.users_get_current_account()


def copen():
    global conn
    global cur
    dbx.files_download_to_file('userdb.sqlite', '/userdb.sqlite')
    # try:
    conn = sqlite3.connect('userdb.sqlite')
    # except:
    #     conn = sqlite3.connect('userdb.sqlite')
    cur = conn.cursor()


def cclose():
    cur.close()
    f = open('userdb.sqlite', 'rb')
    dbx.files_upload(bytes(f.read()), '/userdb.sqlite', mode=dropbox.files.WriteMode.overwrite)
    f.close()



def createtabletodo():
    copen()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS todo (did TEXT, task TEXT)''')
    conn.commit()
    cclose()


def addtodo(uid,task):
    createtabletodo()
    copen()

    cur.execute('''INSERT OR REPLACE INTO todo (did, task)
                        VALUES (?, ?)''', (str(uid), str(task)))
    conn.commit()
    cclose()

def gettodo(uid):
    createtabletodo()
    copen()
    try:
        return cur.execute("SELECT task FROM todo WHERE did LIKE ? ",(uid,)).fetchall()
    except IndexError:
        return False


def createtableuserdb():
    copen()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users (did TEXT UNIQUE, dname TEXT, usern TEXT UNIQUE, rating INTEGER)''')
    conn.commit()
    cclose()


def adduser(did, dname, usern, rating):
    copen()
    createtableuserdb()
    cur.execute('''INSERT OR REPLACE INTO Users (did, dname, usern, rating)
                    VALUES (?, ?, ?, ?)''', (str(did), str(dname), str(usern), int(rating)))
    conn.commit()
    cclose()


def searchuser(usern):
    createtableuserdb()
    copen()

    usern = '%' + usern + '%'
    try:
        return cur.execute("SELECT rating, dname FROM Users WHERE dname LIKE ? ", (usern,)).fetchall()[0]
    except IndexError:
        return False
    cclose()



def searchid(id):
    createtableuserdb()
    copen()

    try:
        return cur.execute("SELECT rating FROM Users WHERE handle LIKE ? ", (id,)).fetchall()[0][0]
    except IndexError:
        return False
    cclose()


def printdb():
    createtableuserdb()
    copen()

    x = []
    for row in cur.execute('SELECT * FROM Users'):
        x.append([str(row[0]), str(row[1]) , row[2], row[3]])
    return x
    cclose()

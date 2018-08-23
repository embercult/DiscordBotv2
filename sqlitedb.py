import sqlite3
import dropbox
import os
import codechefcrawlerv2 as cc
from struct import pack


token1 = str(os.environ.get('TOKENDB', 3))
dbx = dropbox.Dropbox(token1)
dbx.users_get_current_account()


def copen():
    global conn
    global cur
    print('trying to get stuff from dropbox then')
    dbx.files_download_to_file('userdb.sqlite','/userdb.sqlite')
    #parsed = parser.from_buffer(file_contents)
    # try:w
    conn = sqlite3.connect('userdb.sqlite')
    #     conn = sqlite3.connect('userdb.sqlite')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Users (did TEXT UNIQUE, dname TEXT, usern TEXT UNIQUE, rating INTEGER)''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todo (did TEXT, task TEXT)''')
    conn.commit()

def cclose():
    cur.close()
    f = open('userdb.sqlite', 'rb')
    dbx.files_upload(bytes(f.read()), '/userdb.sqlite', mode=dropbox.files.WriteMode.overwrite)
    f.close()


def addtodo(uid,task):
    
    copen()

    cur.execute('''INSERT OR REPLACE INTO todo (did, task)
                        VALUES (?, ?)''', (str(uid), str(task)))
    conn.commit()
    cclose()

def gettodo(uid):
    
    copen()
    try:
        return cur.execute("SELECT task FROM todo WHERE did LIKE ? ",(uid,)).fetchall()
    except IndexError:
        return False

def deltodo(uid):
    
    copen()
    cur.execute("DELETE FROM todo WHERE did LIKE ? ",(uid,)).fetchall()
    conn.commit()
    cclose()


def adduser(did, dname, usern, rating):

    
    copen()
    cur.execute('''INSERT OR REPLACE INTO Users (did, dname, usern, rating)
                    VALUES (?, ?, ?, ?)''', (str(did), str(dname), str(usern), int(rating)))
    conn.commit()
    cclose()


def searchuser(usern):
    
    copen()

    usern = '%' + usern + '%'
    try:
        x =  cur.execute("SELECT rating, dname FROM Users WHERE dname LIKE ? ", (usern,)).fetchall()[0]
        cclose()
        return x
    except IndexError:
        cclose()
        return False




def searchid(id):
    
    copen()

    try:
        x = cur.execute("SELECT rating FROM Users WHERE handle LIKE ? ", (id,)).fetchall()[0][0]
        cclose()
        return x
    except IndexError:
        cclose()
        return False



def updatedb():
    
    copen()
    x = cur.execute("SELECT did, usern FROM Users").fetchall()
    for i in range(len(x)):
        rat = cc.user_rating(x[i][1])
        # print(rat , x[i][1])
        cur.execute('''UPDATE Users SET rating = ? WHERE did = ?''', (str(rat), str(x[i][0])))
    conn.commit()
    cclose()


def printdb():
    
    copen()

    x = []
    for row in cur.execute('SELECT * FROM Users'):
        x.append([str(row[0]), str(row[1]) , row[2], row[3]])
    cclose()
    return x


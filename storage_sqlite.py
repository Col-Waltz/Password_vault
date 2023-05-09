import sqlite3

connection = sqlite3.connect('server')
crsr = connection.cursor()
crsr.execute("""CREATE TABLE IF NOT EXISTS Users (user_id TEXT, org_name TEXT, login TEXT, password TEXT, PRIMARY KEY (user_id,org_name))""")
connection.commit()

def new_user(user_id):
    crsr.execute("""SELECT user_id FROM Users""")
    res = crsr.fetchall()
    if user_id in res:
        return 1
    else:
        return 0

def add_new_user(user_id):
    return 

def org_name_check(user_id,org_name):
    crsr.execute("""SELECT COUNT(*) FROM Users WHERE user_id = ? AND org_name = ?""",(user_id,org_name))
    res = crsr.fetchall()
    if res[0][0] != 0:
        return True
    else:
        return False

def storage_empty(user_id):
    crsr.execute('SELECT COUNT(*) FROM Users WHERE user_id = \n'+str(user_id)+'\n')
    res = crsr.fetchall()
    if res[0][0] == 0:
        return 1
    else:
        return 0

def push_data(user_id,data):
    crsr.execute("""REPLACE INTO Users VALUES (?,?,?,?)""",(user_id,data['organization'],data['login'],data['password']))
    connection.commit()

def get_login(user_id,org_name):
    crsr.execute("""SELECT login FROM Users WHERE user_id=? AND org_name=?""",(user_id,org_name))
    res = crsr.fetchall()
    return res[0][0]

def get_password(user_id,org_name):
    crsr.execute("""SELECT password FROM Users WHERE user_id=? AND org_name=?""",(user_id,org_name))
    res = crsr.fetchall()
    return res[0][0]

def pop_data(user_id,data):
    crsr.execute("""DELETE FROM Users WHERE user_id=? AND org_name=?""",(user_id,data['organization']))
    connection.commit()

def get_all_orgs(user_id):
    crsr.execute('SELECT org_name FROM Users WHERE user_id = \n'+str(user_id)+'\n')
    orgs = []
    res = crsr.fetchall()
    for typle in res:
        orgs.append(typle[0])
    return orgs
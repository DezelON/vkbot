import configs
import logging
from databaseApi import DataBaseConnection

dbConnection = DataBaseConnection()

def createUser(id):
    dbConnection.connection()
    if len(dbConnection.select(table="users", where="userid={0}".format(id)))==0:
        dbConnection.insert(table="users", set="userid={0}, can_write=False, can_notify=False, message_cursor=0".format(id))
    dbConnection.disconnection()

def createUsers(ids):
    dbConnection.connection()
    for id in ids:
        if len(dbConnection.select(table="users", where="userid={0}".format(id)))==0:
            dbConnection.insert(table="users", set="userid={0}, can_write=True, can_notify=False, message_cursor=0".format(id))
    dbConnection.disconnection()

def getUser(id):
    dbConnection.connection()
    answer = dbConnection.select(table="users", where="userid={0}".format(id))
    dbConnection.disconnection()
    if len(answer) == 0:
        return None
    else:
        return answer[0]

def canWrite(id):
    user = getUser(id)
    if user is None:
        return None
    else:
        return bool(getUser(id)["can_write"])

def getAllUsers():
    dbConnection.connection()
    answer = dbConnection.select(table="users")
    dbConnection.disconnection()
    return answer

def getUsersCanNotify(can_notify=True):
    dbConnection.connection()
    answer = dbConnection.select(table="users", where="can_write=True, can_notify={0}".format(can_notify))
    dbConnection.disconnection()
    if len(answer) == 0:
        return None
    else:
        return bool(answer[0]['can_notify'])

def getUsersCanWrite(can_write=True):
    dbConnection.connection()
    answer = dbConnection.select(table="users", where="can_write={0}".format(can_write))
    dbConnection.disconnection()
    if len(answer) == 0:
        return None
    else:
        return bool(answer[0]['can_write'])

def allowWriteUser(id):
    dbConnection.connection()
    dbConnection.update(table="users", set="can_write=True", where="userid={0}".format(id))
    dbConnection.disconnection()

def disableWriteUser(id):
    dbConnection.connection()
    dbConnection.update(table="users", set="can_write=False", where="userid={0}".format(id))
    dbConnection.disconnection()

def allowNotifyUser(id):
    dbConnection.connection()
    dbConnection.update(table="users", set="can_notify=True", where="userid={0}".format(id))
    dbConnection.disconnection()

def disableNotifyUser(id):
    dbConnection.connection()
    dbConnection.update(table="users", set="can_notify=False", where="userid={0}".format(id))
    dbConnection.disconnection()

def setCursorMessageUser(id, cursorid):
    dbConnection.connection()
    dbConnection.update(table="users", set="message_cursor={0}".format(cursorid), where="userid={0}".format(id))
    dbConnection.disconnection()

def getCursorMessageUser(id):
    dbConnection.connection()
    answer = dbConnection.select(table="users", data="message_cursor", where="userid={0}".format(id))
    dbConnection.disconnection()
    if len(answer) == 0:
        return None
    else:
        return str(answer[0]['message_cursor'])

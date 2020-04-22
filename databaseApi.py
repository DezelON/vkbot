import configs
import pymysql

from pymysql.cursors import DictCursor

class DataBaseConnection:

    def __init__(self, dbname=configs.dbName, user=configs.dbUser, password=configs.dbPassword, host=configs.dbHost):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.conn = None
        self.cursor = None
        self._connection()

    def _connection(self):
        if not self.conn is None:
            self._disconnection()
        self.conn = pymysql.connect(db=self.dbname, user=self.user, password=self.password, host=self.host, charset='utf8mb4', cursorclass=DictCursor)
        self.cursor = self.conn.cursor()

    def _disconnection(self):
        if not self.cursor is None:
            self.cursor.close()
            self.cursor = None
        if not self.conn is None:
            self.conn.close()
            self.conn = None

    def connection(self):
        self._connection()

    def disconnection(self):
        self._disconnection()

    def select(self, **kwargs):

        _data = "*"
        _from = None
        _where = None

        answer = []

        for key, value in kwargs.items():
            if key == "data":
                _data = value
            elif key == "table":
                _from = value
            elif key == "where":
                _where = value

        if _from is None:
            return None

        query = "SELECT {0} FROM {1}".format(_data, _from)

        if not _where is None:
            query+= " WHERE {}".format(_where)

        self.cursor.execute(query)

        for row in self.cursor:
            answer.append(row)

        return answer

    def insert(self, **kwargs):

        _into = None
        _set = None
        _sets = None

        for key, value in kwargs.items():
            if key == "table":
                _into = value
            elif key == "set":
                _set = value
            elif key == "sets":
                _sets = value

        if _into is None or (_set is None and _sets is None):
            return None

        if not _sets is None:
            for elem in _sets:
                query = "INSERT INTO {0} SET {1}".format(_into, elem)
                self.cursor.execute(query)

        if not _set is None:
            query = "INSERT INTO {0} SET {1}".format(_into, _set)
            self.cursor.execute(query)

        self.conn.commit()

        return "OK"

    def update(self, **kwargs):

        _table = None
        _set = None
        _where = None

        for key, value in kwargs.items():
            if key == "table":
                _table = value
            elif key == "set":
                _set = value
            elif key == "where":
                _where = value

        if _table is None or _set is None:
            return None

        query = "UPDATE {0} SET {1}".format(_table, _set)

        if not _where is None:
            query += " WHERE {}".format(_where)

        self.cursor.execute(query)
        self.conn.commit()

        return "OK"

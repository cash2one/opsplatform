# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: store.py
@time: 16-6-23 上午11:20
"""

import MySQLdb
from opsplatform.settings import *


def connect_db(host, port, user, password, db):
    try:
        conn = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=db,
            use_unicode=True,
            charset="utf8")
        return conn
    except Exception, e:
        print "Fatal: connect db fail:%s" % e
        return None


class DB(object):

    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.db = db
        self._conn = connect_db(self.host, self.port, self.user, self.password, self.db)

    def connect(self):
        self._conn = connect_db(self.host, self.port, self.user, self.password, self.db)
        return self._conn

    def execute(self, *a, **kw):
        cursor = kw.pop('cursor', None)
        try:
            cursor = cursor or self._conn.cursor()
            cursor.execute(*a, **kw)
        except (AttributeError, MySQLdb.OperationalError):
            self._conn and self._conn.close()
            self.connect()
            cursor = self._conn.cursor()
            cursor.execute(*a, **kw)
        return cursor

    def commit(self):
        if self._conn:
            try:
                self._conn.commit()
            except MySQLdb.OperationalError:
                self._conn and self._conn.close()
                self.connect()
                self._conn and self._conn.commit()

    def rollback(self):
        if self._conn:
            try:
                self._conn.rollback()
            except MySQLdb.OperationalError:
                self._conn and self._conn.close()
                self.connect()
                self._conn and self._conn.rollback()

graph_db_conn = DB(
        GRAPH_DB_HOST,
        GRAPH_DB_PORT,
        GRAPH_DB_USER,
        GRAPH_DB_PASSWORD,
        GRAPH_DB_DATABASE)

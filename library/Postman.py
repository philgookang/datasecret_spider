import mysql.connector
from mysql.connector import errorcode
import json
import sys
import os

class Postman:

    # postan singleton
    singleton = None

    # mysql connection
    mysqlConnection = None

    # mysql cursor
    mysqlCursor = None

    @staticmethod
    def init():

        if Postman.singleton == None:

            # create new object
            Postman.singleton = Postman()

            # create new connection
            Postman.singleton.connect()

        return Postman.singleton


    def connect(self):

        def get_config():
            with open("./database.config") as f:
                return json.load(f)


        config = get_config()

        # get database config
        username    = config["user"]
        password    = config["password"]
        host        = config["host"]
        database    = "datasecret"

        # connection to database
        self.mysqlConnection = mysql.connector.connect(user=username, password=password, host=host, database=database, charset="utf8", raise_on_warnings=True)

        # makes life easy
        self.mysqlConnection.autocommit = True

        # create cusor
        self.mysqlCursor = self.mysqlConnection.cursor(dictionary=True, buffered=True)

        # set names
        self.mysqlCursor.execute("SET NAMES " + config["connection"])


    def execute(self, sql, params = [], show_sql = False):

        try:

            # execute sql
            self.mysqlCursor.execute( sql, tuple(params) )

        except  mysql.connector.Error as err:
            
            print("[MYSQL ERROR] " , err)

            # connection has gone away, lets reconnect and start over again!
            if err.errno == 2006:

                # reconnect to database
                self.connect()

                # recursively call execute again
                return self.execute(sql, params, show_sql)

        if show_sql:
            print(self.mysqlCursor.statement)

        return self.mysqlCursor


    def create(self, sql, params = [], show_sql = False):

        result = self.execute(sql, params, show_sql)
        return result.lastrowid


    def getObject(self, sql, params = [], show_sql = False):

        result = self.execute(sql, params, show_sql)

        for row in result:
            return row

        return None


    def getList(self, sql, params = [], show_sql = False):

        result = self.execute(sql, params, show_sql)

        # return list
        list = []

        # loop through result
        for item in result:
            list.append(item)

        return list


    def __del__(self):

        try:

            # clean up cursor
            self.mysqlCursor.close()

            # clean up mysql
            self.mysqlConnection.close()

        except (AttributeError, ReferenceError) as e:
            pass


    def __exit__(self, exc_type, exc_value, traceback):

        # clean up cursor
        self.mysqlCursor.close()

        # clean up mysql
        self.mysqlConnection.close()



p = Postman.init()
#p.connect()


# conexion a bases de datos y metodos de actualizacion
#


from operator import indexOf
from unittest import result
import mysql.connector
from mysql.connector import errorcode, cursor
import json
# parametros de conexion.

#_HOST = 'Host Name'
#_USER = 'User Name'
#_PASSWORD = 'Password Name'
#_DATABASE = 'Database Name'


class sql_conexion:
    cursor = cursor
    conexion = mysql.connector
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
    
    def connect(self):
        try: 
            self.conexion = mysql.connector.connect(user=self.user, password=self.password,
                            host=self.host, database = self.database)    
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                error = "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                error = "Database does not exist"
        finally:
            error = "Connected"
            return [error]

    def execute(self, sql):
        # execute SQL statements
        # stmt is type of SQL statement = 'SELECT, UPDATE, DELETE, INSERT'
        try:
            self.cursor.execute(sql)
            if 'SELECT' in str(sql).upper():
                results = self.cursor.fetchall()
                return results
            else:
                self.conexion.commit()
                return {'errno':0, 'description':'Done'}
        except mysql.connector.Error as err:
            return {'errno':err.errno,'description':err}

    def close(self):
        try:
            self.conexion.close()
        except mysql.connector.Error as err:
            return {'errno':err.errno,'description':err}

        return True

###########
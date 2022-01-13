import mysql.connector
from mysql.connector import errorcode, cursor

class db_connection:
    def __init__(self, user, password, host, database, as_dict):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.error = ''
        self.db_connector = mysql.connector
        self.cn_cursor = cursor
        self.as_dict = as_dict

    def __repr__(self, error) -> str:
        self.error = error
        return(print(error))

    def open(self):
        try:
            self.db_connector = mysql.connector.connect(user=self.user, password=self.password,
                              host=self.host,
                              database=self.database)
            if self.as_dict:
                self.cn_cursor = self.db_connector.cursor(dictionary=True)
            else:
                self.cn_cursor = self.db_connector.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.error = "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.error = "Database does not exist"
            else:
                self.error = err
        else:
            self.error = 'Successfull'
            return self.db_connector

    def close(self):
        self.db_connector.close
        self.error = "database Close"



""" user_db = db_connection('root', '', 'localhost','users', False)
user_db.open()
db_cursor = user_db.cn_cursor
db_cursor.execute("select username from users")

for(user) in db_cursor:
    print (user)  """
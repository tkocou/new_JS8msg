## a class object to handle all sql processing

import sqlite3

class DB_object():
    ## some class level variables
    #conn = ""
    #cur = ""
    #SQL_message = ""

    
    ## When we create a new object, we pass the database file name to this class
    ## The reason for the set* and exec* methods is for assisting with debugging.
    ##    db_file is a string
    def __init__ (self,db_file):
        super().__init__()
        
        self.sql_result = None
        
        ## init a handler for SQL messages
        try:
            self.SQL_message = ""
            self.conn = sqlite3.connect(db_file)
            self.cur = self.conn.cursor()
            return None
        except:
            return sqlite3.DatabaseError
        
    def set_SQL(self, message):
        ## message will be a SQL command string
        ## example listed next:
        ## """CREATE TABLE setting (id    INTEGER PRIMARY KEY AUTOINCREMENT, name  TEXT    UNIQUE ON CONFLICT IGNORE, value TEXT)"""
        self.SQL_message = message
        #print("Received message: ",message)
    
    def exec_SQL(self):
        try:
            self.sql_result = self.cur.execute(self.SQL_message)
            self.conn.commit()
            return True, self.sql_result
        except:
            ## return SQL error
            return False, self.sql_result
        
    def fetch_all_SQL(self):
        try:
            self.cur.execute(self.SQL_message)
            self.sql_result = self.cur.fetchall()
            return True, self.sql_result
        except:
            ## return SQL error
            return False, self.sql_result
        
    def fetch_once_SQL(self):
        try:
            self.cur.execute(self.SQL_message)
            self.sql_result = self.cur.fetchone()
            return True, self.sql_result
        except:
            ## return SQL error
            return False, self.sql_result
        
    
    def close_SQL(self):
        self.conn.close()